from typing import Generator

from app.core.config import settings
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from databases import Database


DATABASE_URL = settings.DATABASE_URL
engine = create_engine(DATABASE_URL)
database = Database(DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db() -> Generator:
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()
