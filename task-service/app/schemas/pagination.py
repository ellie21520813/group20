from pydantic import BaseModel, EmailStr
from typing import Any, List


class Pagination(BaseModel):
    current: int = 1
    pageSize: int = 5

class PaginationShow(BaseModel):
    current: int
    pageSize: int
    total: int
    class Config: # to convert non dict obj to json
        orm_mode = True

