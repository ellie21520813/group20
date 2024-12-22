from app.db.base_class import Base
from sqlalchemy import (Column, Integer, String, Boolean)
from sqlalchemy.orm import relationship


class File(Base):
    id = Column(Integer, primary_key=True, index=True)
    file_id = Column(String, nullable=False, unique=True)
    name = Column(String, nullable=False)
    size = Column(Integer, nullable=False)
    ext = Column(String)
    type = Column(String, nullable=False)
    local_url = Column(String, nullable=True)
    is_public = Column(Boolean, default=False)
    # public_url = Column(String)
    created_by = Column(String, nullable=False)