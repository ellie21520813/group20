from pydantic import BaseModel, EmailStr
from fastapi import UploadFile
from datetime import datetime

class FileCreate(BaseModel):
    file_id: str
    name: str
    size: int
    type: str
    ext: str
    local_url: str
    is_public: bool
    created_by: str


class FileShow(BaseModel):
    id: int
    file_id: str
    name: str
    size: int
    ext: str
    type: str
    local_url: str
    is_public: bool
    created_by: str
    created_date: datetime
    class Config: # to convert non dict obj to json
        orm_mode = True