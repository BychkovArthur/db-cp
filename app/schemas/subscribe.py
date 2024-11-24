from pydantic import BaseModel, ConfigDict

class RegisterSubscribe(BaseModel):
    user_id1: int
    user_id2: int
    battle_type_id: int
    
    model_config = ConfigDict(from_attributes=True)