import cv2
import io
import glob
import subprocess
import signal
import imutils
import os
import asyncio
import time

from fastapi import APIRouter, HTTPException, status
from fastapi import Depends, Response, Request
from fastapi import WebSocket, WebSocketDisconnect
from fastapi.responses import HTMLResponse
from fastapi.responses import FileResponse, StreamingResponse

from sqlalchemy.orm import Session
# from app.db.session import get_db
from app.core.config import settings
from app.deps.auth import get_current_user_from_token
from app.schemas.pagination import Pagination, PaginationShow
from app.schemas.camera import Camera
from app.schemas.pagination_res import PaginationResponse

from multiprocessing import Process, Queue
from imutils.video import VideoStream
from sse_starlette.sse import EventSourceResponse
from starlette.websockets import WebSocketState
from datetime import datetime

camera_ws_router = APIRouter()
os.environ["OPENCV_FFMPEG_CAPTURE_OPTIONS"] = "rtsp_transport;udp"

class ConnectionManager:
    def __init__(self):
        self.active_connections: list[dict] = []

    async def connect(self, camera_id, websocket: WebSocket):
        await websocket.accept()
        self.disconnect(camera_id)
        self.active_connections.append({'camera_id': camera_id, 'socket': websocket})

    def disconnect(self, camera_id: str):
        self.active_connections = [item for item in self.active_connections if item['camera_id'] != camera_id]

    def get_socket_by_id(self, camera_id):
        for item in self.active_connections: 
            if item['camera_id'] == camera_id:
                return item

    async def send_personal_message(self, message: str, websocket: WebSocket):
        await websocket.send_text(message)

    async def broadcast(self, message: str):
        for connection in self.active_connections:
            await connection.send_text(message)

manager = ConnectionManager()
@camera_ws_router.websocket('/{camera_id}')
async def test_ws(
    camera_id: int,
    url: str,
    websocket: WebSocket,
):
    try:
        await websocket.accept()
        face_cascade = cv2.CascadeClassifier('xml/haarcascade_frontalface_default.xml') 
        capture = cv2.VideoCapture(url)
        capture.set(cv2.CAP_PROP_BUFFERSIZE, 0)
        while websocket.application_state == WebSocketState.CONNECTED:
            ret, img = capture.read() 
            if ret:
                img = cv2.resize(img, (320, 180))
                gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY) 
                faces = face_cascade.detectMultiScale(gray, 1.3, 5)
                for (x,y,w,h) in faces: 
                    cv2.rectangle(img,(x,y),(x+w,y+h),(255,255,0),2)  
                # if faces != ():
                res, im_png = cv2.imencode(".jpg", img)
                if res:
                    await websocket.send_bytes(im_png.tobytes())
                    
        await websocket.close()
        capture.release()
    except WebSocketDisconnect:
        capture.release()
        return