from datetime import timedelta

from app.core.config import settings
from app.core.hashing import Hasher
from app.core.security import create_access_token
from app.db.repository.login import get_user, get_user_by_email
from app.db.session import get_db
from app.db.models.users import User
from app.schemas.tokens import Token
from app.schemas.user import ShowUser

from app.deps.auth import get_current_user_from_token

from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException
from fastapi import status
from fastapi import Response
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.encoders import jsonable_encoder

from sqlalchemy.orm import Session


login_router = APIRouter()


def authenticate_user(username: str, password: str, db: Session = Depends(get_db)):
    user: User = get_user(username=username, db=db)
    if not user:
        user: User = get_user_by_email(email=username, db=db)
        if not user:
            return False

    if not Hasher.verify_password(password, user.hashed_password):
        return False
    
    return user


@login_router.post("/token", response_model=Token)
def login_for_access_token(
    response: Response,
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    user: ShowUser = authenticate_user(form_data.username, form_data.password, db)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password"
        )
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Your account is not activated!!!!"
        )
    
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"username": user.username}, expires_delta=access_token_expires
    )
    response.set_cookie(
        key="access_token", value=f"Bearer {access_token}", httponly=True
    )
    
    return {"access_token": access_token, "token_type": "bearer", "user": user}


@login_router.get("/me", response_model=ShowUser)
def get_me(user: User = Depends(get_current_user_from_token), db: Session = Depends(get_db)):
    return user


@login_router.post("/logout")
def logout(response: Response):
    response.delete_cookie("access_token")
    return {"message": "Logged out!"}


