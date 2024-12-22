from app.db.session import get_db
from app.schemas.role import RoleCreate
from app.schemas.role import ShowRole
from app.deps.auth import get_current_user_from_token
from app.db.models.users import User
from app.db.repository.role import *


from fastapi import APIRouter, HTTPException, status
from fastapi import Depends
from sqlalchemy.orm import Session
from typing import List


role_router = APIRouter()


@role_router.get(
    "/all", 
    response_model=List[ShowRole],
    summary="Get a list of all roles"
)
def all_role(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user_from_token)
):
    if not current_user.is_superuser:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="You are not permitted!!!!"
        )
    role = get_all_role(db=db)
    return role


@role_router.post("/create-role", response_model=ShowRole)
def create_role(
    role: RoleCreate, 
    current_user: User = Depends(get_current_user_from_token), 
    db: Session = Depends(get_db)
):
    if not current_user.is_superuser:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="You are not permitted!!!!"
        )
    role = create_new_role(role, db)
    return role


@role_router.delete("/{role_id}", response_model=ShowRole)
def delete_user(
    role_id: int,
    current_user: User = Depends(get_current_user_from_token), 
    db: Session = Depends(get_db)
):
    if current_user.is_superuser:
        role = delete_role(id=role_id, db=db)
        return {"msg": "Successfully deleted.", "detail": role}
    
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="You are not permitted!!!"
    )