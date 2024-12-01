from pydantic import BaseModel, ConfigDict
from typing import Optional


class CreateUserDetailedInfo(BaseModel):
    crowns: int
    max_crowns: int
    clan_id: Optional[int] = None

    model_config = ConfigDict(from_attributes=True)


class UpdateUserDetailedInfo(BaseModel):
    id: int
    crowns: Optional[int] = None
    max_crowns: Optional[int] = None
    clan_id: Optional[int] = None

    model_config = ConfigDict(from_attributes=True)
