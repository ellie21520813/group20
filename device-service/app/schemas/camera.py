from pydantic import BaseModel, EmailStr
from fastapi import UploadFile
from typing import Union
from datetime import datetime


class CameraCreate(BaseModel):
    name: str
    ip: str
    port: int
    stream_path: str
    protocol: str
    owner: str

class RtspCamera(BaseModel):
    id: int
    ip: str
    port: int
    protocol: str
    username: Union[str, None]
    password: Union[str, None]
    url: str
    path: Union[str, None]
    owner: str
    class Config:
        orm_mode = True

class CameraShow(BaseModel):
    class Config: # to convert non dict obj to json
        orm_mode = True
