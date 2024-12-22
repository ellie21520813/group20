from fastapi import APIRouter, HTTPException, status
from fastapi import Depends
from fastapi.responses import HTMLResponse

from app.schemas.task import CreateTask, TaskShow, TaskUpdate, TaskStatusUpdate

from sqlalchemy.orm import Session
from starlette.websockets import WebSocket, WebSocketDisconnect

from app.db.session import get_db
from app.core.config import settings
from app.deps.auth import get_current_user_from_token
from app.schemas.pagination import Pagination, PaginationShow
from app.schemas.pagination_res import TaskPaginationResponse
from app.services.rabbitmq.rabbitmq import Notifier

import app.db.repository.task as TaskRepository

task_router = APIRouter()


@task_router.websocket("/queue")
async def websocket_endpoint(websocket: WebSocket, queue: str):
    notifier = Notifier()
    await notifier.connect(websocket)
    await notifier.setup(queue)
    try:
        while True:
            data = await websocket.receive_text()
            # await websocket.send_text(f"Message text was: {data}")
    except WebSocketDisconnect:
        await notifier.remove()

@task_router.post("", response_model=TaskPaginationResponse)
async def get_all_tasks(
    pagination: Pagination,
    user = Depends(get_current_user_from_token),
    db: Session = Depends(get_db)
):
    return TaskRepository.get_all_task(user['username'], pagination, db);

@task_router.post("/create-task", response_model=TaskShow)
async def create_new_task(
    task: CreateTask,
    db: Session = Depends(get_db),
    user: str = Depends(get_current_user_from_token),
):
    task = TaskRepository.create_new_task(task, user['username'], db)
    return task

@task_router.post("/service/{service}", response_model=TaskPaginationResponse)
async def get_all_tasks_by_service(
    service: str,
    pagination: Pagination,
    user = Depends(get_current_user_from_token),
    db: Session = Depends(get_db)
):
    return TaskRepository.get_all_task_by_service(service, user['username'], pagination, db);

@task_router.post("/update/{id}", response_model=TaskShow)
async def update_task(
    id: int, 
    task: TaskUpdate,
    db: Session = Depends(get_db),
    user = Depends(get_current_user_from_token)
):
    task = TaskRepository.update_task(id, task, user['username'], db)
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Not found task!!!!"
        )
    return task

@task_router.post("/change-status/{id}", response_model=TaskShow)
async def change_task_status(
    id: int,
    new_status: TaskStatusUpdate,
    db: Session = Depends(get_db),
    user = Depends(get_current_user_from_token)
):
    task = TaskRepository.change_status(id, user['username'], new_status, db)
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Not found task!!!!"
        )
    return task

@task_router.delete("/delete/{id}", response_model=TaskShow)
async def delete_task(
    id: int,
    db: Session = Depends(get_db),
    user = Depends(get_current_user_from_token)
):
    task = TaskRepository.delete_task(id, user['username'], db)
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Not found task!!!!"
        )
    return task