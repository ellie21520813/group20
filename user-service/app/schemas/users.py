from pydantic import BaseModel, EmailStr
from typing import Any, List, Union
from datetime import datetime, date
from app.schemas.user_role import ShowUserRole


class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str
    first_name: str
    last_name: str
    sex: int
    birthday: date
    language: str
    phone: str


class ShowRole(BaseModel):
    role_id: int
    detail: str

    class Config: # to convert non dict obj to json
        orm_mode = True

class ShowUser(BaseModel):
    id: Any
    username: str
    email: EmailStr
    email_verified: bool
    first_name: str
    last_name: str
    avatar: Union[str, None]
    sex: int
    birthday: date
    language: str
    phone: str
    phone_verified: bool
    is_active: bool
    is_superuser: bool
    roles: List[ShowUserRole]

    class Config: # to convert non dict obj to json
        orm_mode = True