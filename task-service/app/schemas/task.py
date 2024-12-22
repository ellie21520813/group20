from pydantic import BaseModel, EmailStr
from fastapi import UploadFile
from datetime import datetime
from typing import List, Union


class CreateTask(BaseModel):
    name: str
    description: Union[str, None]
    ramq_queue: Union[str, None]
    service: Union[str, None]
    status: Union[str, None]

class TaskUpdate(BaseModel):
    name: Union[str, None]
    description: Union[str, None]
    status: Union[str, None]
    ramq_queue: Union[str, None]
    # service: Union[str, None]
    output: Union[str, None]

class TaskStatusUpdate(BaseModel):
    status: str

class TaskShow(BaseModel):
    id: int
    name: Union[str, None]
    description: Union[str, None]
    ramq_queue: Union[str, None]
    status: Union[str, None]
    service: Union[str, None]
    output: Union[str, None]
    created_by: Union[str, None]
    created_date: Union[datetime, None]
    updated_date: Union[datetime, None]
    class Config: # to convert non dict obj to json
        orm_mode = True
