from fastapi import APIRouter, Depends, status

from app.db import SessionDep
from app.schemas.battle_type import CreateBattleType
from app.services.battle_type import BattleTypeService

router = APIRouter(tags=["BattleType"], prefix="/battle_type")


@router.post("/register", status_code=status.HTTP_201_CREATED)
async def register_battle_type(
    data: CreateBattleType,
    session: SessionDep,
):
    return await BattleTypeService.register_battle_type(data, session)

