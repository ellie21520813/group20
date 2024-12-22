import uuid

from app.db.models.device_token import DeviceToken
from app.schemas.device_token import DeviceTokenCreate, DeviceTokenShow
from app.schemas.pagination import Pagination

from sqlalchemy import or_
from sqlalchemy.orm import Session

from datetime import datetime


def add_token(token: DeviceTokenCreate, owner: str, db: Session):
    token: DeviceToken = DeviceToken(
        description = token.description,
        token=uuid.uuid4(),
        enable=True,
        owner=owner
    )
    db.add(token)
    db.commit()
    db.refresh(token)
    return token


def get_all_token(pagination: Pagination, db: Session):
    if pagination.current == 0:
        pagination.current = 1
    offset = pagination.pageSize * (pagination.current-1)
    tokens = db.query(DeviceToken).order_by(DeviceToken.id.desc()).limit(pagination.pageSize).offset(offset=offset).all()
    total = db.query(DeviceToken).count()

    pagination_result = {
        "current": pagination.current,
        "pageSize": pagination.pageSize,
        "total": total
    }

    return {"data": tokens, "pagination": pagination_result}

def get_all_token_of_user(pagination: Pagination, owner: str, db: Session):
    if pagination.current == 0:
        pagination.current = 1
    offset = pagination.pageSize * (pagination.current-1)
    tokens = db.query(DeviceToken).filter(DeviceToken.owner==owner).order_by(DeviceToken.id).limit(pagination.pageSize).offset(offset=offset).all()
    total = db.query(DeviceToken).count()

    pagination_result = {
        "current": pagination.current,
        "pageSize": pagination.pageSize,
        "total": total
    }

    return {"data": tokens, "pagination": pagination_result}

def get_token_by_id(id: int, db: Session):
    token: DeviceToken = db.query(DeviceToken).filter(DeviceToken.id == id).first()
    if not token:
        return None
    return token

def get_token_by_token(token: str, db: Session):
    token = db.query(DeviceToken).filter(DeviceToken.token == token).first()
    if not token:
        return None
    return token

def validate_token(token: str, db: Session):
    token = db.query(DeviceToken).filter(DeviceToken.token == token).first()
    if not token:
        return False
    return True

def delete_token(id: int, db: Session):
    token = db.query(DeviceToken).filter(DeviceToken.id == id).first()
    if not token:
        return None
    db.delete(token)
    db.commit()
    return token