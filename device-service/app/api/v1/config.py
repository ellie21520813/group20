import app.db.respository.config as ConfigRepository
import app.db.respository.device as DeviceRepository

from fastapi import APIRouter, HTTPException, status, WebSocket
from fastapi import Depends
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.core.config import settings
from app.deps.auth import get_current_user_from_token
from app.db.models.config import DeviceConfig
from app.db.models.device import Device
from app.schemas.config import ConfigCreate, ConfigShow, AddConfigShow
from app.schemas.camera import RtspCamera
from app.schemas.pagination import Pagination, PaginationShow
from app.schemas.pagination_res import PaginationResponse


config_route = APIRouter()

@config_route.get("/rtsp/{device_id}", response_model=RtspCamera)
def get_rtsp_config(
    device_id: int,
    user = Depends(get_current_user_from_token),
    db: Session = Depends(get_db)
):
    device: Device = DeviceRepository.get_device_by_device_id(device_id=device_id, owner=user['username'], db=db)
    
    port: DeviceConfig = ConfigRepository.get_config_by_key(device_id=device_id, key="PORT", db=db)
    ip: DeviceConfig = ConfigRepository.get_config_by_key(device_id=device_id, key="IP", db=db)
    username: DeviceConfig = ConfigRepository.get_config_by_key(device_id=device_id, key="USERNAME", db=db)
    password: DeviceConfig = ConfigRepository.get_config_by_key(device_id=device_id, key="PASSWORD", db=db)
    path: DeviceConfig = ConfigRepository.get_config_by_key(device_id=device_id, key="PATH", db=db)
    protocol: DeviceConfig = ConfigRepository.get_config_by_key(device_id=device_id, key="PROTOCOL", db=db)
    
    ip = ip.value if ip != None else ""
    port = port.value if port != None else ""
    username = username.value if username != None else ""
    password = password.value if password != None else ""
    path = path.value if path != None else ""
    protocol = protocol.value.lower() if protocol != None else ""

    if username != "":
        stream_url = f"{protocol}://{username}:{password}@{ip}:{port}{path}"
    else:
        stream_url = f"{protocol}://{ip}:{port}{path}"

    res = RtspCamera(
        id=device.device.id,
        ip=ip,
        port=int(port),
        username=username,
        password=password,
        protocol=protocol,
        path=path,
        url=stream_url,
        owner=device.device.owner
    )

    return res

@config_route.post("/add", response_model=AddConfigShow)
def add_config(
    config: ConfigCreate, 
    db: Session = Depends(get_db),
    user: str = Depends(get_current_user_from_token)
):
    try:
        config = ConfigRepository.add_config(config_create=config, owner=user['username'], db=db)
        return config
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Key already exists!"
        )

@config_route.delete("/{id}", response_model=ConfigShow)
def delete_config(
    id: int, 
    db: Session = Depends(get_db),
    user: str = Depends(get_current_user_from_token)
):
    config: DeviceConfig = ConfigRepository.get_config_by_id(id=id, db=db)
    if not user["is_superuser"] or user['username'] != config.owner:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You are not permitted!!!!"
        )
    config = ConfigRepository.delete_config(id=id, db=db)
    return config

@config_route.get("/{id}", response_model=ConfigShow)
def get_config(
    id: int,
    user = Depends(get_current_user_from_token),
    db: Session = Depends(get_db)
):
    config: DeviceConfig = ConfigRepository.get_config_by_id(id=id, db=db)
    if not config:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND
        )
    if not user["is_superuser"] or config.owner != user['username']:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You are not permitted!!!!"
        )
    return config

@config_route.post("/{device_id}/all", response_model=PaginationResponse[ConfigShow])
def get_config(
    device_id: str,
    pagination: Pagination,
    user = Depends(get_current_user_from_token),
    db: Session = Depends(get_db)
):
    try:
        configs: DeviceConfig = ConfigRepository.get_config_by_device_id(device_id=device_id, pagination=pagination, db=db)
        return configs
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    
@config_route.get("/{device_id}/{key}")
def get_config_by_key(
    device_id: int,
    key: str,
    user = Depends(get_current_user_from_token),
    db: Session = Depends(get_db)
):
    config: DeviceConfig = ConfigRepository.get_config_by_key(device_id=device_id, key=key, db=db)
    if user['username'] != config.owner:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="You are not permitted!"
        )
    return config