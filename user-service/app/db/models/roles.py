from app.db.base_class import Base
from sqlalchemy import (Column, Integer, String)
from sqlalchemy.orm import relationship


class Role(Base):
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    detail = Column(String, nullable=True)