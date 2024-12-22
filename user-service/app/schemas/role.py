from pydantic import BaseModel, EmailStr
from typing import Any


class RoleCreate(BaseModel):
    name: str
    detail: str


class ShowRole(RoleCreate):
    id: int
    
    class Config: # to convert non dict obj to json
        orm_mode = True
 