import os

class Settings:
    VERSION =  'v1'
    DATABASE_URL = os.getenv("DATABASE_URL")
    SECRET_KEY :str = "404cfadbb8335b315a781542ae3ad67b6467f0d362b642eb619198aa534819bf"
    ALGORITHM = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES = 24*60
    RABBITMQ_HOST = os.getenv("RABBITMQ_HOST")
    RABBITMQ_USER = os.getenv("RABBITMQ_USER")
    RABBITMQ_PASS = os.getenv("RABBITMQ_PASS")
    
settings = Settings()