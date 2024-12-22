from app.db.models.config import DeviceConfig
from app.schemas.config import ConfigCreate
from app.schemas.pagination import Pagination

from sqlalchemy import or_, and_
from sqlalchemy.orm import Session

from datetime import datetime

def add_config(config_create: ConfigCreate, db: Session, owner: str = ""):
    res = []
    for config in config_create.configs:
        res.append(config)
        config = DeviceConfig(
            device_id=config_create.device_id,
            key=config.key,
            value=config.value,
            owner=owner
        )
        db.add(config)
    db.commit()
    return {
        "device_id": config_create.device_id,
        "configs": res,
    }
    
def get_config_by_device_id(device_id: str, pagination: Pagination, db: Session):
    if pagination.current == 0:
        pagination.current = 1
    offset = pagination.pageSize * (pagination.current-1)
    # get device and check owner -> get device config: todo later

    config = db.query(DeviceConfig).filter(DeviceConfig.device_id==device_id).order_by(DeviceConfig.id).limit(pagination.pageSize).offset(offset=offset).all()
    total = db.query(DeviceConfig).filter(DeviceConfig.device_id==device_id).count()
    pagination_result = {
        "current": pagination.current,
        "pageSize": pagination.pageSize,
        "total": total
    }
    return {"data": config, "pagination": pagination_result}

def get_config_by_id(id: int, db: Session):
    config = db.query(DeviceConfig).filter(DeviceConfig.id==id).first()
    if not config:
        return None
    return config

def get_config_by_key(device_id: int, key: str, db: Session):
    config = db.query(DeviceConfig).filter(and_(DeviceConfig.device_id==device_id, DeviceConfig.key==key)).first()
    if not config:
        return None
    return config

def delete_config(id: int, db: Session):
    config = db.query(DeviceConfig).filter(DeviceConfig.id == id).first()
    if not config:
        return None
    db.delete(config)
    db.commit()
    return config

def delete_config_by_device_id(device_id: str, db: Session):
    config = db.query(DeviceConfig).filter(DeviceConfig.device_id == device_id).all()
    if not config:
        return None
    db.delete(config)
    db.commit()
    return config