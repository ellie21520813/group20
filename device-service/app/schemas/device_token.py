from pydantic import BaseModel, EmailStr
from typing import Union
from datetime import datetime


class DeviceTokenCreate(BaseModel):
    description: Union[str, None]
    

class DeviceTokenShow(BaseModel):
    id: int
    token: str
    description: Union[str, None]
    enable: bool
    device_id: Union[str, None]
    owner: Union[str, None]
    updated_date: Union[datetime, None]

    class Config: # to convert non dict obj to json
        orm_mode = True
