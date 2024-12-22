from typing import Dict, Union, Optional
from pydantic import BaseModel

from fastapi import HTTPException
from fastapi import Request
from fastapi import status
from fastapi.openapi.models import OAuthFlows
from fastapi.security import OAuth2
import os
import httpx

from fastapi.security.utils import get_authorization_scheme_param
from fastapi import Depends

from jose import JWTError, jwt

from app.core.config import settings


def get_me(token):
    USER_SERVICE_HOST_URL = 'http://user-service:8000'
    url = os.environ.get("USER_SERVICE_HOST_URL") or USER_SERVICE_HOST_URL
    headers = {
        "Authorization": f"Bearer {token}"
    }
    response = httpx.get(f'{url}/api/v1/user/me', headers=headers)
    return response.json()

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
        
        user = get_me(token=token)
        return user
    except JWTError:
        raise credentials_exception
