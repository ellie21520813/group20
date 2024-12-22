import app.db.respository.device as DeviceRepository

from fastapi import APIRouter, HTTPException, status, WebSocket
from fastapi import Depends
from fastapi.responses import HTMLResponse
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.core.config import settings
from app.deps.auth import get_current_user_from_token
from app.db.models.device import Device
from app.schemas.device import DeviceCreate, DeviceShow, DeviceConfigShow
from app.schemas.pagination import Pagination, PaginationShow
from app.schemas.pagination_res import PaginationResponse


device_router = APIRouter()


@device_router.post('/all', response_model=PaginationResponse[DeviceShow])
async def get_all_devices(
    pagination: Pagination,
    user: str = Depends(get_current_user_from_token),
    db: Session = Depends(get_db)
):
    if user["is_superuser"]:
        return DeviceRepository.get_all_device(pagination=pagination, db=db)
    else:
        return DeviceRepository.get_all_device(pagination=pagination, db=db, owner=user['username'])

@device_router.get("/{device_id}", response_model=DeviceConfigShow)
def get_device_info(
    device_id: int,
    user = Depends(get_current_user_from_token),
    db: Session = Depends(get_db)
):
    device: Device = DeviceRepository.get_device_by_device_id(device_id=device_id, owner=user['username'], db=db)
    return device

@device_router.post("/add")
def add_device(
    device: DeviceCreate, 
    db: Session = Depends(get_db),
    user = Depends(get_current_user_from_token)
):
    device = DeviceRepository.add_device(device_add=device, db=db, owner=user['username'])
    return device

@device_router.delete("/{device_id}", response_model=DeviceShow)
def delete_device(
    device_id: str, 
    db: Session = Depends(get_db),
    user: str = Depends(get_current_user_from_token)
):
    device: Device = DeviceRepository.get_device_by_device_id(device_id=device_id, db=db, owner=user['username'])
    if not user["is_superuser"] and device.owner != user['username']:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You are not permitted!!!!"
        )
    device = DeviceRepository.delete_device(device_id=device_id, db=db)
    return device
