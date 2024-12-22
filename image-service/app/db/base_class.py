import datetime

from typing import Any
from sqlalchemy import (Column, Integer, String, Boolean, DateTime)
from sqlalchemy.ext.declarative import as_declarative
from sqlalchemy.ext.declarative import declared_attr
from fastapi import Depends

@as_declarative()
class Base:
    id: Any
    __name__: str
    # created_date = Column(DateTime, default=datetime.datetime.utcnow)
    # updated_date = Column(DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)
    
    # to generate table from classname
    @declared_attr
    def __tablename__(cls) -> str:
        return cls.__name__.lower()