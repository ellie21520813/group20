from pydantic import BaseModel, EmailStr
from typing import Any, Union, Optional
from datetime import date

class ShowUser(BaseModel):
    id: Any
    username: str
    avatar: Optional[str] = None
    email: EmailStr
    email_verified: bool
    first_name: str
    last_name: str
    sex: int
    birthday: date
    language: str
    phone: str
    phone_verified: bool
    is_active: bool
    is_superuser: bool
    roles: Any

    class Config: # to convert non dict obj to json
        orm_mode = True