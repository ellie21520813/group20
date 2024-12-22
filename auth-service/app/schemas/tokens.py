from pydantic import BaseModel
from app.schemas.user import ShowUser

class Token(BaseModel):
    access_token: str
    token_type: str
    user: ShowUser