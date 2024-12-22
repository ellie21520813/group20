from pydantic import BaseModel, EmailStr
from fastapi import UploadFile
from typing import Union
from datetime import datetime
from typing import Union, List

class Config(BaseModel):
    key: str
    value: str

class ConfigCreate(BaseModel):
    device_id: int
    configs: List[Config]

class AddConfigShow(BaseModel):
    device_id: int
    configs: List[Config]
    # owner: str

class ConfigShow(BaseModel):
    id: int
    device_id: int
    key: str
    value: str
    owner: str

    class Config: # to convert non dict obj to json
        orm_mode = True
