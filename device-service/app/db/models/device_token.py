import datetime

from app.db.base_class import Base
from sqlalchemy import (Column, Integer, Float, String, Boolean, DateTime)
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import relationship


class DeviceToken(Base):
    id = Column(Integer, primary_key=True, index=True)
    token = Column(String, nullable=False)
    description = Column(String)
    enable = Column(Boolean)
    device_id = Column(String)
    owner = Column(String)
    created_date = Column(DateTime, default=datetime.datetime.utcnow)
    updated_date = Column(DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)
    