from pydantic import BaseModel, EmailStr
from typing import Any, List, Union


class Camera(BaseModel):
    id: int = 1
    ip: str = "192.168.x.x"
    port: int = 554
    protocol: str = "rtsp"
    username: Union[str, None]
    password: Union[str, None]
    path: Union[str, None]
    url: str
    owner: str
