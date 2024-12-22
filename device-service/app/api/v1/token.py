import app.db.respository.device_token as DeviceTokenRepository

from fastapi import APIRouter, HTTPException, status, WebSocket
from fastapi import Depends
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.core.config import settings
from app.deps.auth import get_current_user_from_token
from app.db.models.device_token import DeviceToken
from app.schemas.device_token import DeviceTokenCreate, DeviceTokenShow
from app.schemas.pagination import Pagination, PaginationShow
from app.schemas.pagination_res import PaginationResponse


token_router = APIRouter()


@token_router.post('/all', response_model=PaginationResponse[DeviceTokenShow])
async def get_all_token(
    pagination: Pagination,
    user: str = Depends(get_current_user_from_token),
    db: Session = Depends(get_db)
):
    if not user["is_superuser"]:
        return DeviceTokenRepository.get_all_token_of_user(pagination=pagination, owner=user['username'], db=db)
    else:
        return DeviceTokenRepository.get_all_token(pagination=pagination, db=db)

@token_router.get("/{id}", response_model=DeviceTokenShow)
def get_token(
    id: int,
    user = Depends(get_current_user_from_token),
    db: Session = Depends(get_db)
):
    token: DeviceToken = DeviceTokenRepository.get_token_by_id(id=id, db=db)
    if not user["is_superuser"] and token.owner != user['username']:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You are not permitted!!!!"
        )
    return token

@token_router.get("/validate/{token}", response_model=DeviceTokenShow)
def validate_token(
    token: str,
    db: Session = Depends(get_db)
):
    if not token:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Token invalid!"
        )
    return token


@token_router.post("/add", response_model=DeviceTokenShow)
def create_token(
    token: DeviceTokenCreate, 
    db: Session = Depends(get_db),
    user: str = Depends(get_current_user_from_token)
):
    token = DeviceTokenRepository.add_token(token=token, owner=user['username'], db=db)
    return token

@token_router.delete("/{id}", response_model=DeviceTokenShow)
def delete_device(
    id: int, 
    db: Session = Depends(get_db),
    user: str = Depends(get_current_user_from_token)
):
    token: DeviceToken = DeviceTokenRepository.get_token_by_id(id=id, db=db)
    if not user["is_superuser"] and user['username'] != token.owner:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You are not permitted!!!!"
        )
    token = DeviceTokenRepository.delete_token(id=id, db=db)
    return token
