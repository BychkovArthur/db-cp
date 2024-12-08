from fastapi import Depends, HTTPException, status
from fastapi.responses import JSONResponse
from fastapi.security import OAuth2PasswordRequestForm

from datetime import timedelta
from typing import Annotated

from jose import JWTError, jwt
from loguru import logger
from sqlalchemy.ext.asyncio import AsyncSession

from app.daos import user, user_detailed_info, clan
from app.db import get_session
from app.models.user import User as UserModel
from app.schemas.token import Token, TokenData
from app.schemas.user import ChangePasswordIn, UserRegister, UserOut
from app.services.utils import UtilsService, oauth2_scheme
from app.settings import settings

from .royale_api_client import api_client


class UserService:
    @staticmethod
    async def register_user(user_data: UserRegister, session: AsyncSession):
        user_exist = await UserService.user_email_exists(session, user_data.email)

        if user_exist:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="User with the given email already exists!!!",
            )

        user_tag = user_data.tag.upper()
        
        try:
            player = await api_client.get_player(user_tag)
        except:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Invalig ClashRoyale User Tag: {user_tag}"
            )
        
        crowns = player['trophies']
        max_crowns = player['bestTrophies']
        name = player['name']
        _clan = player.get('clan')
        
        clan_id = None
        if _clan:
            clan_id = (await clan.ClanDao(session).create({
                "name": _clan["name"],
                "tag": _clan["tag"][1:]
            })).id
        
        new_user_detailed_info = await user_detailed_info.UserDetailedInfoDao(session).create({
            "crowns": crowns,
            "max_crowns" : max_crowns,
            "clan_id" : clan_id
        })
        
        user_data.password = UtilsService.get_password_hash(user_data.password)
        
        new_user = await user.UserDao(session).create({
            "email": user_data.email,
            "password": user_data.password,
            "tag": user_tag,
            "name": name,
            "user_detailed_info_id": new_user_detailed_info.id
        })
        await session.commit()
        logger.info(f"New user created successfully: {new_user}!!!")
        return JSONResponse(
            content={"message": "User created successfully"},
            status_code=status.HTTP_201_CREATED,
        )

    @staticmethod
    async def authenticate_user(session: AsyncSession, email: str, password: str) -> UserModel | bool:
        _user = await user.UserDao(session).get_by_email(email)
        if not _user or not UtilsService.verify_password(password, _user.password):
            return False
        return _user

    @staticmethod
    async def user_email_exists(session: AsyncSession, email: str) -> UserModel | None:
        _user = await user.UserDao(session).get_by_email(email)
        return _user if _user else None

    @staticmethod
    async def login(form_data: OAuth2PasswordRequestForm, session: AsyncSession) -> Token:
        _user = await UserService.authenticate_user(session, form_data.username, form_data.password)
        if not _user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Incorrect email or password",
            )

        access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = UtilsService.create_access_token(data={"sub": _user.email}, expires_delta=access_token_expires)
        token_data = {
            "access_token": access_token,
            "token_type": "Bearer",
        }
        return Token(**token_data)

    @staticmethod
    async def get_current_user(
        session: AsyncSession = Depends(get_session),
        token: str = Depends(oauth2_scheme),
    ) -> UserModel:
        credentials_exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
            email: str = payload.get("sub")
            if not email:
                raise credentials_exception
            token_data = TokenData(email=email)
        except JWTError:
            raise credentials_exception
        _user = await user.UserDao(session).get_by_email(email=token_data.email)
        if not _user:
            raise credentials_exception
        return _user

    @staticmethod
    async def get_all_users(session: AsyncSession) -> list[UserOut]:
        all_users = await user.UserDao(session).get_all()
        return [UserOut.model_validate(_user) for _user in all_users]
    
    @staticmethod
    async def get_all_users_except_self(
        session: AsyncSession,
        current_user: UserModel
    ) -> list[UserOut]:
        users = await user.UserDao(session).get_all_except_self(current_user.id)
        user_ids = [_user.user_detailed_info_id for _user in users]
        users_detailed_info = await user_detailed_info.UserDetailedInfoDao(session).get_by_ids(user_ids)
        
        user_detailed_info_id_to_object = {info.id: info for info in users_detailed_info}
        
        user_out_list = []
        for _user in users:
            detailed_info = user_detailed_info_id_to_object.get(_user.user_detailed_info_id)
            crowns = detailed_info.crowns if detailed_info else 0
            max_crowns = detailed_info.max_crowns if detailed_info else 0
            
            user_out = UserOut(
                id=_user.id,
                name=_user.name,
                crowns=crowns,
                max_crowns=max_crowns
            )
            user_out_list.append(user_out)
        
        return user_out_list
        
    

    @staticmethod
    async def delete_all_users(session: AsyncSession):
        await user.UserDao(session).delete_all()
        return JSONResponse(
            content={"message": "All users deleted successfully!!!"},
            status_code=status.HTTP_200_OK,
        )

    @staticmethod
    async def change_password(
        password_data: ChangePasswordIn,
        current_user: UserModel,
        session: AsyncSession = Depends(get_session),
    ):
        if not UtilsService.verify_password(password_data.old_password, current_user.password):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Incorrect old password!!!",
            )
        current_user.password = UtilsService.get_password_hash(password_data.new_password)
        session.add(current_user)
        await session.commit()
        return JSONResponse(
            content={"message": "Password updated successfully!!!"},
            status_code=status.HTTP_200_OK,
        )

    @staticmethod
    async def get_user_by_id(user_id: int, session: AsyncSession) -> UserOut:
        _user = await user.UserDao(session).get_by_id(user_id)
        if not _user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User with the given id does not exist!!!",
            )
        return UserOut.model_validate(_user)

    @staticmethod
    async def delete_user_by_id(user_id: int, session: AsyncSession):
        _user = await user.UserDao(session).delete_by_id(user_id)
        if not _user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User with the given id does not exist!!!",
            )
        return JSONResponse(
            content={"message": "User deleted successfully!!!"},
            status_code=status.HTTP_200_OK,
        )


CurrentUserDep = Annotated[UserModel, Depends(UserService.get_current_user)]
