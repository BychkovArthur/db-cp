from pydantic import BaseModel, ConfigDict


class CreateClan(BaseModel):
    name: str

    model_config = ConfigDict(from_attributes=True)


class UpdateClan(BaseModel):
    id: int
    name: str

    model_config = ConfigDict(from_attributes=True)
