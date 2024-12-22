from app.core.hashing import Hasher
from app.db.models.roles import Role
from app.schemas.role import RoleCreate

from sqlalchemy.orm import Session


def create_new_role(role_create: RoleCreate, db: Session):
    role = Role(
        name=role_create.name,
        detail=role_create.detail
    )

    db.add(role)
    db.commit()
    db.refresh(role)
    return role


def get_all_role(db: Session):
    role = db.query(Role).all()
    return role

def get_role_by_id(id: int, db: Session):
    role = db.query(Role).filter(id==id).first()
    return role

def delete_role(id: int, db: Session):
    role = db.query(Role).filter(id==id).first()
    db.delete(role)
    db.commit()
    return role
