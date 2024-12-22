import os

class Settings:
    VERSION =  'v1'
    DATABASE_URL = os.getenv("DATABASE_URI")
    SECRET_KEY :str = "404cfadbb8335b315a781542ae3ad67b6467f0d362b642eb619198aa534819bf"
    ALGORITHM = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES = 100*24*60

settings = Settings()