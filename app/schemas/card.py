from pydantic import BaseModel, ConfigDict


class CreateCard(BaseModel):
    name: str
    type: str
    level: int

    model_config = ConfigDict(from_attributes=True)


class UpdateCard(BaseModel):
    id: int
    name: str
    type: str
    level: int

    model_config = ConfigDict(from_attributes=True)
