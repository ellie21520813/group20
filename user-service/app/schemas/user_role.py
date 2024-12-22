from pydantic import BaseModel, EmailStr
from typing import Any


class ShowUserRole(BaseModel):
    user_id: int
    role_id: int
    
    class Config: # to convert non dict obj to json
        orm_mode = True
 