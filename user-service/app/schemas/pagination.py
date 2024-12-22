from pydantic import BaseModel, EmailStr, Field
from typing import Any, List


class Pagination(BaseModel):
    current: int = Field(default=1)
    pageSize: int = Field(default=5)

class PaginationShow(BaseModel):
    current: int
    pageSize: int
    total: int
    class Config: # to convert non dict obj to json
        orm_mode = True