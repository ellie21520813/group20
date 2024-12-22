import app.db.respository.device as DeviceRepository
import app.db.respository.device_token as DeviceTokenRepository

from fastapi import APIRouter, HTTPException, status
from fastapi import WebSocket, WebSocketDisconnect
from fastapi import Depends
from fastapi.responses import HTMLResponse
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.core.config import settings
from app.deps.auth import get_current_user_from_token
from app.schemas.device import DeviceCreate, DeviceShow
from app.schemas.pagination import Pagination, PaginationShow
from app.schemas.pagination_res import PaginationResponse
from datetime import datetime


ws_router = APIRouter()

class ConnectionManager:
    def __init__(self):
        self.active_connections: list[dict] = []

    async def connect(self, device_id, websocket: WebSocket):
        await websocket.accept()
        self.disconnect(device_id)
        self.active_connections.append({'device_id': device_id, 'socket': websocket})

    def disconnect(self, device_id: str):
        self.active_connections = [item for item in self.active_connections if item['device_id'] != device_id]

    def get_socket_by_id(self, device_id):
        for item in self.active_connections: 
            if item['device_id'] == device_id:
                return item

    async def send_personal_message(self, message: str, websocket: WebSocket):
        await websocket.send_text(message)

    async def broadcast(self, message: str):
        for connection in self.active_connections:
            await connection.send_text(message)


manager = ConnectionManager()


@ws_router.websocket("/command/{device_id}/{token}")
async def device_cmd(
    websocket: WebSocket,
    device_id: str,
    token: str
):
    await manager.connect(device_id, websocket)
    try:
        try:
            while True:
                db = next(get_db())
                token_valid = DeviceTokenRepository.validate_token(token=token, db=db)
                db.close()
                if not token_valid:
                    raise WebSocketDisconnect 
                message = await websocket.receive_json()
                to = message['send']['to']
                to_ws = manager.get_socket_by_id(to)
                # print(f"\tTo: {to_ws['device_id']}")
                # print(f"\tMessage: {message}")
                await to_ws['socket'].send_json(message)

        except Exception as e:
            print(e)            

    except WebSocketDisconnect:
        manager.disconnect(device_id)
        status='disconnected'
        db = next(get_db())
        DeviceRepository.update_status(device_id=device_id, status=status, db=db)
    


@ws_router.websocket("/info/{device_id}/{token}")
async def device_info(
    websocket: WebSocket, 
    device_id: str,
    token: str,
):
    await manager.connect(device_id, websocket)
    try:
        while True:
            try:
                db = next(get_db())
                token_valid = DeviceTokenRepository.validate_token(token=token, db=db)
                db.close()
                if not token_valid:
                    raise WebSocketDisconnect 
                device = await websocket.receive_json()
                device_add = DeviceCreate(
                    device_id=device['id'],
                    name=device['name'],
                    hostname=device['hostname'],
                    ip=device['ip'],
                    machine=device['machine'],
                    version=device['version'],
                    platform=device['platform'],
                    system=device['system'],
                    processor=device['processor'],
                    cpu=device['cpu'],
                    memory=str(device['memory']),
                    status=device['status']
                )
                db = next(get_db())
                DeviceRepository.save_device(device_add=device_add, db=db)
                db.close()
            except WebSocketDisconnect:
                raise WebSocketDisconnect
            except Exception as e:
                print(e)
                
    except WebSocketDisconnect:
        manager.disconnect(websocket)
        status='disconnected'
        db = next(get_db())
        DeviceRepository.update_status(device_id=device_id, status=status, db=db)
        db.close()
