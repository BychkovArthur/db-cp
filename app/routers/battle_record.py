from fastapi import APIRouter, Depends, status, HTTPException

from app.db import SessionDep
from app.services.user import CurrentUserDep
from app.services.battle_record import BattleRecordService
from app.schemas.battle_record import BattleRecordOut, AggregatedBattleRecord

router = APIRouter(tags=["BattleRecord"], prefix="/battle_records")

@router.get("/", response_model=list[BattleRecordOut], status_code=status.HTTP_200_OK)
async def get_current_user_battle_records(
    session: SessionDep,
    current_user: CurrentUserDep
):
    return await BattleRecordService.get_battle_records(current_user, session)


@router.get("/aggregated/", response_model=list[AggregatedBattleRecord], status_code=status.HTTP_200_OK)
async def get_aggregated_battle_records(
    session: SessionDep,
    current_user: CurrentUserDep
):
    return await BattleRecordService.get_aggregated_battle_records(current_user, session)