from app.schemas.file import FileShow
from app.schemas.pagination import PaginationShow
from typing import List
from pydantic import BaseModel


class FilePaginationResponse(BaseModel):
    data: List[FileShow]
    pagination: PaginationShow