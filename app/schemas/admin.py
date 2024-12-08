from pydantic import BaseModel

class RestoreDumpRequest(BaseModel):
    filename: str