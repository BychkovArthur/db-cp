from pydantic import BaseModel, ConfigDict
from typing import Optional, List


class CreateBattleRecord(BaseModel):
    subscribe_id: int
    user1_score: int
    user2_score: int
    user1_get_crowns: int
    user2_get_crowns: int
    user1_card_ids: List[int]
    user2_card_ids: List[int]
    replay: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)


class UpdateBattleRecord(BaseModel):
    id: int
    subscribe_id: Optional[int] = None
    user1_score: Optional[int] = None
    user2_score: Optional[int] = None
    user1_get_crowns: Optional[int] = None
    user2_get_crowns: Optional[int] = None
    user1_card_ids: Optional[List[int]] = None
    user2_card_ids: Optional[List[int]] = None
    replay: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)
