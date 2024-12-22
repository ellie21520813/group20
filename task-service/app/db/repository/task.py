from app.db.models.task import Task
from app.schemas.task import CreateTask, TaskUpdate, TaskStatusUpdate
from app.schemas.pagination import Pagination

from sqlalchemy import or_, and_
from sqlalchemy.orm import Session


def get_all_task(username: str, pagination: Pagination, db: Session):
    if pagination.current == 0:
        pagination.current = 1
    offset = pagination.pageSize * (pagination.current-1)
    tasks = db.query(Task).filter(Task.created_by == username).order_by(Task.id.desc()).limit(pagination.pageSize).offset(offset).all()
    total_count = db.query(Task).filter(Task.created_by == username).count()
    pagination_result = {
        "current": pagination.current,
        "pageSize": pagination.pageSize,
        "total": total_count
    }
    return {"data": tasks, "pagination": pagination_result}

def get_all_task_by_service(service: str, username: str, pagination: Pagination, db: Session):
    if pagination.current == 0:
        pagination.current = 1
    offset = pagination.pageSize * (pagination.current-1)
    tasks = db.query(Task).filter(and_(Task.created_by == username, Task.service == service)).order_by(Task.id.desc()).limit(pagination.pageSize).offset(offset).all()
    total_count = db.query(Task).filter(Task.created_by == username).count()
    pagination_result = {
        "current": pagination.current,
        "pageSize": pagination.pageSize,
        "total": total_count
    }
    return {"data": tasks, "pagination": pagination_result}


def create_new_task(task: CreateTask, username: str, db: Session):
    task = Task(
        name=task.name,
        description=task.description,
        ramq_queue=task.ramq_queue,
        service=task.service,
        status=task.status,
        created_by=username,    
    )
    db.add(task)
    db.commit()
    return task

def update_task(task_id, task_update: TaskUpdate, user: str, db: Session):
    task: Task = db.query(Task).filter(and_(Task.created_by == user, Task.id == task_id)).first()
    if not task:
        return None
    
    for a in task_update:
        key, value = a
        if value:
            setattr(task, key, value)
    db.commit()
    return task

def delete_task(id: int, user: str, db: Session):
    task: Task = db.query(Task).filter(and_(Task.created_by == user, Task.id == id)).first()
    if not task:
        return None
    db.delete(task)
    db.commit()
    return task

def change_status(task_id: int, user: str, status: TaskStatusUpdate, db: Session):
    task: Task = db.query(Task).filter(and_(Task.created_by == user, Task.id == task_id)).first()
    if not task:
        return None
    task.status = status.status
    db.commit()
    return task