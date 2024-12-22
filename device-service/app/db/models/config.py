import datetime

from app.db.base_class import Base
from sqlalchemy import Column, Integer, Float, String, Sequence
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import relationship


class DeviceConfig(Base):
    __tablename__ = 'deviceconfig'
    id_sec = Sequence(__tablename__ + "_id_seq")
    id = Column(Integer, id_sec, server_default=id_sec.next_value(), nullable=False)
    device_id = Column(Integer, primary_key=True, nullable=False)
    key = Column(String, primary_key=True, nullable=False)
    value = Column(String, nullable=False)
    owner = Column(String)