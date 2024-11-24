from fastapi import Depends, HTTPException, status
from fastapi.responses import JSONResponse

from datetime import timedelta
from typing import Annotated

from loguru import logger
from sqlalchemy.ext.asyncio import AsyncSession

from app.daos import battle_type
from app.db import get_session
from app.schemas.battle_type import RegisterBattleType
from app.settings import settings

from .royale_api_client import api_client


class BattleTypeService:
    @staticmethod
    async def register_battle_type(data: RegisterBattleType, session: AsyncSession):
        new_battle_type = await battle_type.BattleTypeDao(session).create(data.model_dump())
        
        logger.info(f"New battle_type created successfully: {new_battle_type}!!!")
        return JSONResponse(
            content={"message": "BattleType created successfully"},
            status_code=status.HTTP_201_CREATED,
        )