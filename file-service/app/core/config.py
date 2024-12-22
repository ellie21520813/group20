import os

class Settings:
    VERSION =  'v1'
    DATABASE_URL = os.getenv("DATABASE_URI")
    SECRET_KEY :str = "404cfadbb8335b315a781542ae3ad67b6467f0d362b642eb619198aa534819bf"
    ALGORITHM = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES = 24*60
    MAX_SIZE_UPLOAD = 10*1024*1024
    UPLOAD_FOLDER = f"/{os.path.abspath(os.curdir)}/app/upload"
    FILE_NAME_LENGTH = 10
settings = Settings()