from pydantic import BaseModel, ConfigDict


class CreateSubscribe(BaseModel):
    user_id1: int
    user_id2: int
    battle_type_id: int

    model_config = ConfigDict(from_attributes=True)


class UpdateSubscribe(BaseModel):
    id: int
    user_id1: int
    user_id2: int
    battle_type_id: int

    model_config = ConfigDict(from_attributes=True)


class SubscriptionOut(BaseModel):
    user_id1: int
    user_id2: int
    battle_type: int
    
    model_config = ConfigDict(from_attributes=True)