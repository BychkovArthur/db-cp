from pydantic import BaseModel, ConfigDict


class CreateBattleType(BaseModel):
    name: str
    
    model_config = ConfigDict(from_attributes=True)


class UpdateBattleType(BaseModel):
    id: int
    name: str
    
    model_config = ConfigDict(from_attributes=True)
