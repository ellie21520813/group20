from app.schemas.task import TaskShow
from app.schemas.pagination import PaginationShow
from typing import List
from pydantic import BaseModel


class TaskPaginationResponse(BaseModel):
    data: List[TaskShow]
    pagination: PaginationShow