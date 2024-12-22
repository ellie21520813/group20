from app.db.base_class import Base
from sqlalchemy import (Boolean, Column, Integer, String, DateTime)
from sqlalchemy.orm import relationship

from app.db.models.users_roles import UserRole

class User(Base):
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, nullable=False)
    avatar = Column(String)
    email = Column(String, nullable=False, unique=True, index=True)
    email_verified = Column(Boolean, default=False)
    first_name = Column(String)
    last_name = Column(String)
    sex = Column(Integer)
    birthday = Column(DateTime)
    language = Column(String)
    phone = Column(String)
    phone_verified = Column(Boolean, default=False)

    hashed_password = Column(String, nullable=False)
    is_active = Column(Boolean(), default=True)
    is_superuser = Column(Boolean(), default=False)
    roles = relationship("UserRole", back_populates="user")