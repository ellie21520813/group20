from app.db.models.file import File
from app.schemas.file import FileCreate
from app.schemas.pagination import Pagination

from sqlalchemy import or_
from sqlalchemy.orm import Session


def create_new_file(file_upload: FileCreate, token: str, db: Session):
    file = File(
        file_id=file_upload.file_id,
        name=file_upload.name,
        ext=file_upload.ext,
        size=file_upload.size,
        type=file_upload.type,
        local_url=file_upload.local_url,
        is_public=file_upload.is_public,
        created_by=file_upload.created_by        
    )
    db.add(file)
    db.commit()
    db.refresh(file)
    return file

def get_all_file(pagination: Pagination, db: Session):
    if pagination.current == 0:
        pagination.current = 1
    offset = pagination.pageSize * (pagination.current-1)

    files = db.query(File).order_by(File.id.desc()).limit(pagination.pageSize).offset(offset=offset).all()
    total_count = db.query(File).count()

    pagination_result = {
        "current": pagination.current,
        "pageSize": pagination.pageSize,
        "total": total_count
    }
    return {"data": files, "pagination": pagination_result}

def get_my_files_and_public(pagination: Pagination, username: str, db: Session):
    if pagination.current == 0:
        pagination.current = 1
    offset = pagination.pageSize * (pagination.current-1)

    files = db.query(File).order_by(File.id.desc()).filter(or_(File.created_by == username, File.is_public)).limit(pagination.pageSize).offset(offset=offset).all()
    total_count = db.query(File).filter(or_(File.created_by == username, File.is_public)).count()

    pagination_result = {
        "current": pagination.current,
        "pageSize": pagination.pageSize,
        "total": total_count
    }
    return {"data": files, "pagination": pagination_result}

def get_my_files(username: str, db: Session):
    files = db.query(File).order_by(File.id).filter(File.created_by == username).all()
    return files

def get_file_by_id(file_id: str, db: Session):
    file = db.query(File).filter(File.file_id == file_id).first()
    return file

def delete_file_by_id(file_id: str, db: Session):
    file = db.query(File).filter(File.file_id == file_id).first()
    db.delete(file)
    db.commit()
    return file