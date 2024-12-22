from app.db.base_class import Base
from sqlalchemy import (Column, Integer, String, Boolean)
from sqlalchemy.orm import relationship


class Task(Base):
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    description = Column(String)
    ramq_queue = Column(String)
    service = Column(String)
    status = Column(String)
    output = Column(String)
    created_by = Column(String, nullable=False)

