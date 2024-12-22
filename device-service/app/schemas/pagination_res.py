from app.schemas.device import DeviceShow
from app.schemas.pagination import PaginationShow
from typing import List, Generic, TypeVar
from pydantic import BaseModel
from pydantic.generics import GenericModel


# class DevicePaginationResponse(BaseModel):
#     data: List[DeviceShow]
#     pagination: PaginationShow

#     class Config: # to convert non dict obj to json
#         orm_mode = True

T = TypeVar('T', bound=BaseModel)
class PaginationResponse(GenericModel, Generic[T]):
    data: List[T]
    pagination: PaginationShow

    class Config: # to convert non dict obj to json
        orm_mode = True
