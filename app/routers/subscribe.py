from fastapi import APIRouter, Depends, status, HTTPException

from app.db import SessionDep
from app.services.user import CurrentUserDep
from app.services.subscribe import (
    SubscribeService,
    CannotSubscribeToSelfError,
    UserNotFoundError,
    SubscriptionExistsError,
    SubscriptionNotFoundError
)

from app.schemas.subscribe import SubscriptionOut

router = APIRouter(tags=["Subscribe"], prefix="/subscriptions")

@router.post("/subscribe/{other_user_id}", status_code=status.HTTP_201_CREATED)
async def subscribe_user(
    session: SessionDep,
    current_user: CurrentUserDep,
    other_user_id: int,
    battle_type_id: int = 1
):
    try:
        subscription = await SubscribeService.subscribe(
            session, current_user, other_user_id, battle_type_id
        )
        return {"message": "Subscription created", "subscription_id": subscription.id}
    except CannotSubscribeToSelfError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Cannot subscribe to yourself."
        )
    except UserNotFoundError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with ID {other_user_id} not found."
        )
    except SubscriptionExistsError:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Subscription already exists for user {current_user.id} to user {other_user_id}."
        )

@router.post("/unsubscribe/{other_user_id}", status_code=status.HTTP_200_OK)
async def unsubscribe_user(
    session: SessionDep,
    current_user: CurrentUserDep,
    other_user_id: int,
    battle_type_id: int = 1
):
    try:
        success = await SubscribeService.unsubscribe(
            session, current_user, other_user_id, battle_type_id
        )
        if success:
            return {"message": "Unsubscribed successfully."}
        else:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Subscription not found."
            )
    except SubscriptionNotFoundError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Subscription not found for user {current_user.id} to user {other_user_id}."
        )
        
@router.get("/", response_model=list[SubscriptionOut], status_code=status.HTTP_200_OK)
async def get_user_subscriptions(
    session: SessionDep,
    current_user: CurrentUserDep
):
    try:
        subscriptions = await SubscribeService.get_subscriptions(session, current_user)
        return [
            SubscriptionOut(
                user_id1=subscription.user_id1,
                user_id2=subscription.user_id2,
                battle_type=subscription.battle_type_id
            ) for subscription in subscriptions
        ]
    except SubscriptionNotFoundError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No subscriptions found for this user."
        )