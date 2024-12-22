import datetime

from app.db.base_class import Base
from sqlalchemy import (Column, Integer, Float, String, Boolean, DateTime)
from sqlalchemy import ForeignKey

class SensorData(Base):
    device_id = Column(String(50), nullable=False)
    sensor = Column(String(50), nullable=False)
    value = Column(String(50), nullable=False)
    token = Column(String(255), nullable=False)
    timestamp = Column(DateTime, default=datetime.datetime.utcnow)