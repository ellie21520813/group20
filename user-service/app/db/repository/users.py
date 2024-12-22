from app.core.hashing import Hasher
from app.db.models.users import User
from app.schemas.users import UserCreate
from app.schemas.pagination import Pagination, PaginationShow
from app.db.models.users_roles import UserRole

from sqlalchemy.orm import Session


def create_new_user(user: UserCreate, db: Session):
    superuser = False
    if user.email == 'baonv@uit.edu.vn':
        superuser = True

    user = User(
        username=user.username,
        email=user.email,
        hashed_password=Hasher.get_password_hash(user.password),
        first_name=user.first_name,
        last_name=user.last_name,
        sex=user.sex,
        birthday=user.birthday,
        language=user.language,
        phone=user.phone,
        is_active=True,
        is_superuser=superuser
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def get_all_user(pagination: Pagination, db: Session):
    if pagination.current == 0:
        pagination.current = 1
    offset = pagination.pageSize * (pagination.current-1)

    users = db.query(User).order_by(User.id).limit(pagination.pageSize).offset(offset=offset).all()
    total_count = db.query(User).count()

    pagination_result = {
        "current": pagination.current,
        "pageSize": pagination.pageSize,
        "total": total_count
    }
    return {"data": users, "pagination": pagination_result}


def get_user_by_email(email: str, db: Session):
    user = db.query(User).filter(User.email == email).first()
    return user


def get_user_by_username(username: str, db: Session):
    user = db.query(User).filter(User.username == username).first()
    return user


def delete_user_by_username(username: str, db: Session):
    user = db.query(User).filter(username==username).first()
    db.delete(user)
    db.commit()
    return user


def set_supper_user(username: str, db: Session):
    user: User = db.query(User).filter(username==username).first()
    user.is_superuser = True
    db.commit()
    return user


def add_user_role(userid: int, roleid: int, db: Session):
    user_role: UserRole = db.query(UserRole.role_id, UserRole.user_id).filter_by(user_id=userid, role_id=roleid).first()
    if not user_role:
        user_role = UserRole(
            user_id = userid,
            role_id = roleid
        )
        db.add(user_role)
        db.commit()
        db.refresh(user_role)
        return user_role
    return user_role