from app.db.models.device import Device
from app.db.models.config import DeviceConfig
from app.schemas.device import DeviceCreate, DeviceConfigShow
from app.schemas.pagination import Pagination

from sqlalchemy import or_, and_
from sqlalchemy.orm import Session

from datetime import datetime

def add_device(device_add: DeviceCreate, db: Session, owner: str = ""):
    device = Device(
        name=device_add.name,
        description=device_add.description,
        enable=device_add.enable,
        owner=owner
    )
    db.add(device)
    db.commit()
    db.refresh(device)
    return device


def get_all_device(pagination: Pagination, db: Session, owner: str = ""):
    if pagination.current == 0:
        pagination.current = 1
    offset = pagination.pageSize * (pagination.current-1)
    if owner != "":
        devices = db.query(Device).filter(Device.owner==owner).order_by(Device.id).limit(pagination.pageSize).offset(offset=offset).all()
    else:
        devices = db.query(Device).order_by(Device.id).limit(pagination.pageSize).offset(offset=offset).all()
    total = db.query(Device).count()

    pagination_result = {
        "current": pagination.current,
        "pageSize": pagination.pageSize,
        "total": total
    }

    db.commit()
    return {"data": devices, "pagination": pagination_result}


def get_device_by_device_id(device_id: int, owner: str, db: Session):
    device: Device = db.query(Device).filter(and_(Device.id==device_id, Device.owner==owner)).first()
    if not device:
        return None
    
    configs = db.query(DeviceConfig).filter(DeviceConfig.device_id == device.id).all()
    res = DeviceConfigShow
    res.device = device
    res.config = configs
    return res

def update_status(device_id: str, status: str, db: Session):
    device: Device = db.query(Device).filter(Device.id == device_id).first()
    if device:
        device.status = status
        db.commit()
    return device

def delete_device(device_id: str, db: Session):
    device = db.query(Device).filter(Device.id == device_id).first()
    if not device:
        return None
    db.delete(device)
    db.query(DeviceConfig).filter(DeviceConfig.device_id == device_id).delete()
    db.commit()
    return device