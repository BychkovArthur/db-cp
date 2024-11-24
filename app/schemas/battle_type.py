from pydantic import BaseModel, ConfigDict

class RegisterBattleType(BaseModel):
    name: str
    
    model_config = ConfigDict(from_attributes=True)