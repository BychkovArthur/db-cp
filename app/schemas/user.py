from pydantic import BaseModel, ConfigDict, EmailStr, field_validator


class UserRegister(BaseModel):
    email: EmailStr
    tag: str
    password: str
    
    model_config = ConfigDict(from_attributes=True)
    

class UserBase(BaseModel):
    email: EmailStr
    name: str
    
    model_config = ConfigDict(from_attributes=True)


class UserIn(UserBase):
    password: str
    
    
class UserOutLogin(UserBase):
    id: int
    name: str
    tag: str
    is_super_user: bool


class UserOut(BaseModel):
    id: int
    name: str
    crowns: int
    max_crowns: int


class ChangePasswordIn(BaseModel):
    old_password: str
    new_password: str

    @field_validator("old_password")
    @classmethod
    def old_password_is_not_blank(cls, value):
        if not value:
            raise ValueError("Old password field can't be blank!!!")
        return value

    @field_validator("new_password")
    @classmethod
    def new_password_is_not_blank(cls, value):
        if not value:
            raise ValueError("New password field can't be blank!!!")
        return value
