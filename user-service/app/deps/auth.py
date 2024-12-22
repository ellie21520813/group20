from typing import Dict, Union, Optional

from fastapi import HTTPException
from fastapi import Request
from fastapi import status
from fastapi.openapi.models import OAuthFlows
from fastapi.security import OAuth2
from fastapi.security.utils import get_authorization_scheme_param
    
from app.core.config import settings
from app.db.repository.login import get_user
from app.db.session import get_db

from fastapi import Depends
from jose import JWTError, jwt
from sqlalchemy.orm import Session


class OAuth2PasswordBearerWithHeader(OAuth2):
    def __init__(
        self,
        tokenUrl: str,
        scheme_name: Union[str, None] = None,
        scopes: Union[Dict[str, str], None] = None,
        auto_error: bool = True
    ):
        if not scopes:
            scopes = {}
        flows = OAuthFlows(password={"tokenUrl": tokenUrl, "scopes": scopes})
        super().__init__(flows=flows, scheme_name=scheme_name, auto_error=auto_error)
    
    async def __call__(self, request: Request) -> Optional[str]:
        authorization: str = request.headers.get(
            "Authorization"
        )

        scheme, param = get_authorization_scheme_param(authorization)
        if not authorization or scheme.lower() != "bearer":
            if self.auto_error:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Not authenticated",
                    headers={"WWW-Authenticate": "Bearer"}
                )
            else:
                return None
        return param

oauth2_scheme = OAuth2PasswordBearerWithHeader(tokenUrl=f"/api/{settings.VERSION}/auth/token")
def get_current_user_from_token(
    token: str  = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
    )
    try:
        payload = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
        )
        username: str = payload.get("username")
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    user = get_user(username=username, db=db)
    if user is None:
        raise credentials_exception
    return user