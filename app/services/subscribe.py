from fastapi import Depends, HTTPException, status
from fastapi.responses import JSONResponse

from datetime import timedelta
from typing import Annotated

from loguru import logger
from sqlalchemy.ext.asyncio import AsyncSession

from app.daos import subscribe, user
from app.models.user import User as UserModel
from app.models.user import Subscribe

class CannotSubscribeToSelfError(Exception):
    pass

class UserNotFoundError(Exception):
    pass

class SubscriptionExistsError(Exception):
    pass

class SubscriptionNotFoundError(Exception):
    pass

class SubscribeService:
    @staticmethod
    async def subscribe(
        session: AsyncSession,
        current_user: UserModel,
        other_user_id: int,
        battle_type_id: int
    ) -> Subscribe:
        if current_user.id == other_user_id:
            raise CannotSubscribeToSelfError("Cannot subscribe to yourself.")
        
        other_user = await user.UserDao(session).get_by_id(other_user_id)
        if not other_user:
            raise UserNotFoundError(f"User with ID {other_user_id} not found.")
        
        existing_subscription = await subscribe.SubscribeDao(session).get_by_triplet(
            current_user.id, other_user_id, battle_type_id
        )
        if existing_subscription:
            raise SubscriptionExistsError(
                f"Subscription already exists for user {current_user.id} to user {other_user_id}."
            )
        
        subscription = await subscribe.SubscribeDao(session).subscribe_user(
            current_user.id, other_user_id, battle_type_id
        )
        return subscription

    @staticmethod
    async def unsubscribe(
        session: AsyncSession,
        current_user: UserModel,
        other_user_id: int,
        battle_type_id: int
    ) -> bool:
        subscription = await subscribe.SubscribeDao(session).get_by_triplet(
            current_user.id, other_user_id, battle_type_id
        )
        if not subscription:
            raise SubscriptionNotFoundError(
                f"Subscription not found for user {current_user.id} to user {other_user_id}."
            )
        
        success = await subscribe.SubscribeDao(session).unsubscribe_user(
            current_user.id, other_user_id, battle_type_id
        )
        return success

    @staticmethod
    async def get_subscriptions(
        session: AsyncSession,
        current_user: UserModel
    ) -> list[Subscribe]:
        subscriptions = await subscribe.SubscribeDao(session).get_subscriptions_by_user(
            current_user.id
        )
        return subscriptions
        