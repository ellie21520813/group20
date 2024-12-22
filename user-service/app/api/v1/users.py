from app.db.session import get_db
from app.schemas.users import ShowUser
from app.schemas.users import UserCreate
from app.schemas.user_role import ShowUserRole
from app.schemas.pagination import Pagination, PaginationShow

from app.deps.auth import get_current_user_from_token
from app.db.models.users import User
from app.db.repository.users import *
from app.db.repository.role import *

from fastapi import APIRouter, HTTPException, status
from fastapi import Depends
from sqlalchemy.orm import Session
from typing import List, Dict


user_router = APIRouter()


from pydantic import BaseModel
class ItemResponse(BaseModel):
    data: List[ShowUser]
    pagination: PaginationShow


@user_router.post(
    "/all", 
    response_model=ItemResponse,
    summary="Get a list of all users"
)
def all_user(
    pagination: Pagination,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user_from_token)
):
    if not current_user.is_superuser:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You are not permitted!!!!"
        )
    users = get_all_user(pagination=pagination, db=db)
    return users


# @user_router.post("/grant-permissions/{username}", response_model=ShowUser)
# def grant_permissions(
#     username: str,
#     db: Session = Depends(get_db),
#     current_user: User = Depends(get_current_user_from_token)
# ):
#     if not current_user.is_superuser:
#         raise HTTPException(
#             status_code=status.HTTP_401_UNAUTHORIZED,
#             detail="You are not permiited!!!"
#         )
#     return set_supper_user(username=username, db=db)


@user_router.post("/signup", response_model=ShowUser)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    user = create_new_user(user=user, db=db)
    return user


@user_router.get("/me", response_model=ShowUser, summary="Get details of currently logged in user")
def get_me(user: User = Depends(get_current_user_from_token)):
    return user


@user_router.delete("/{username}", response_model=ShowUser)
def delete_user(
    username: str,
    current_user: User = Depends(get_current_user_from_token), 
    db: Session = Depends(get_db)
):
    if current_user.is_superuser:
        user = delete_user_by_username(username=username, db=db)
        return {"message": "Successfully deleted.", "detail": user}
    
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="You are not permitted!!!"
    )

@user_router.post("/add-role", response_model=ShowUserRole)
def add_role(
    username: str,
    role_id: int,
    current_user: User = Depends(get_current_user_from_token),
    db: Session = Depends(get_db)
):
    if current_user.is_superuser:
        user: User = get_user_by_username(username=username, db=db)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found!"
            )
        user_id = user.id
        role = get_role_by_id(id=role_id, db=db)
        if not role:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Role not found!!!"
            )
        user_role = add_user_role(userid=user_id, roleid=role_id, db=db)
        return user_role
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="You are not permiited!"
    )