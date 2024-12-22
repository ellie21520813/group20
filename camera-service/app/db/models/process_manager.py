import datetime

from app.db.base_class import Base
from sqlalchemy import Column, Integer, Float, String, Sequence
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import relationship


class ProcessManager(Base):
    id = Column(Integer, primary_key=True)
    process_id = Column(Integer, nullable=False)
    cmd = Column(String, nullable=False)
    custom_field = Column(String)