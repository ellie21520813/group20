from pydantic import BaseModel, EmailStr
from fastapi import UploadFile
from typing import Union, List
from datetime import datetime
from app.schemas.config import ConfigShow

class DeviceCreate(BaseModel):
    name: str
    description: str
    enable: bool

class DeviceShow(BaseModel):
    id: int
    name: str
    description: Union[str, None]
    enable: Union[bool, None]
    updated_date: Union[datetime, None]
    owner: str

    class Config: # to convert non dict obj to json
        orm_mode = True

class DeviceConfigShow(BaseModel):
    device: DeviceShow
    config: List[ConfigShow]

    class Config:
        orm_mode = True