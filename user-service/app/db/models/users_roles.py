from app.db.base_class import Base
from sqlalchemy.orm import relationship
from sqlalchemy import Boolean, Column, Integer, String, ForeignKey


class UserRole(Base):
    user_id = Column(Integer, ForeignKey("user.id"), primary_key=True)
    user = relationship("User", back_populates="roles")
    role_id = Column(Integer, ForeignKey("role.id"), primary_key=True)
    role = relationship("Role")
