import cv2
import io
import glob
import subprocess
import signal
import imutils
import os
import asyncio

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

image_router = APIRouter()
os.environ["OPENCV_FFMPEG_CAPTURE_OPTIONS"] = "rtsp_transport;udp"


@image_router.post('/capture', response_class=FileResponse)
async def capture(
    camera: Camera,
    user = Depends(get_current_user_from_token)
):
    if user['username'] != camera.owner:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="You are not permitted!"
        )

    print(camera.url)
    capture = cv2.VideoCapture(camera.url, cv2.CAP_FFMPEG)
    res, img = capture.read()
    img = cv2.resize(img, (320, 180))
    res, im_png = cv2.imencode(".png", img)
    return StreamingResponse(io.BytesIO(im_png.tobytes()), media_type="image_router/png")

@image_router.post('/face-detect', response_class=FileResponse)
async def face_detect(
    camera: Camera,
    user = Depends(get_current_user_from_token)
):
    face_cascade = cv2.CascadeClassifier('xml/haarcascade_frontalface_default.xml') 
    eye_cascade = cv2.CascadeClassifier('xml/haarcascade_eye.xml')  
    capture = cv2.VideoCapture(camera.url, cv2.CAP_FFMPEG)
    ret, img = capture.read() 
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY) 
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)
    for (x,y,w,h) in faces: 
        cv2.rectangle(img,(x,y),(x+w,y+h),(255,255,0),2)  
        roi_gray = gray[y:y+h, x:x+w] 
        roi_color = img[y:y+h, x:x+w] 
        eyes = eye_cascade.detectMultiScale(roi_gray)  
        for (ex,ey,ew,eh) in eyes: 
            cv2.rectangle(roi_color,(ex,ey),(ex+ew,ey+eh),(0,127,255),2) 
    res, im_png = cv2.imencode(".png", img)
    return StreamingResponse(io.BytesIO(im_png.tobytes()), media_type="image_router/png")

@image_router.post('/start-streaming')
async def start_streaming(
    camera: Camera,
    user = Depends(get_current_user_from_token)
):
    command = f"ps ax | grep ffmpeg | grep camera_{camera.id}"
    for line in os.popen(command): 
        if command not in line and f"camera_{camera.id}" in line:
            print(line)
            return {
                "message": "Camera is already streamming",
                "stream_url": f"http://192.168.1.16/api/v1/camera/stream/camera_{camera.id}.m3u8",
            }
        
    VIDSOURCE=camera.url
    AUDIO_OPTS="-c:a aac -b:a 160000 -ac 2"
    # VIDEO_OPTS="-s 640:320 -c:v libx264 -b:v 800000 -g 150 -force_key_frames 'expr:gte(t,n_forced*10)'"
    VIDEO_OPTS="-s 320:180 -c:v libx264 -b:v 800000"
    OUTPUT_HLS="-hls_time 1 -hls_list_size 10 -start_number 1"
    cmd = f"ffmpeg -i {VIDSOURCE} -y {AUDIO_OPTS} {VIDEO_OPTS} {OUTPUT_HLS} stream/camera_{camera.id}.m3u8"
    process = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True, preexec_fn=os.setsid)

    while not os.path.exists(f"stream/camera_{camera.id}.m3u8"):
        await asyncio.sleep(0.5)

    return {
        "source": VIDSOURCE,
        "audio_opts": AUDIO_OPTS,
        "video_opts": VIDEO_OPTS,
        "output_hls": OUTPUT_HLS,
        "stream_url": f"http://192.168.1.16/api/v1/camera/stream/camera_{camera.id}.m3u8",
        "process_id": process.pid
    }

@image_router.post('/stop-streaming')
async def stop_streaming(
    camera: Camera,
    user = Depends(get_current_user_from_token)
):
    try:
        for line in os.popen(f"ps ax | grep camera_{camera.id}"): 
            fields = line.split()
            pid = fields[0] 
            print(f"Process {pid} be killed")
            os.kill(int(pid), signal.SIGKILL) 
    except:
        pass
    try:
        for f in glob.glob(f"stream/camera_{camera.id}*"):
            print(f"Removed file: {f}")
            os.remove(f)
    except:
        pass
    return {
        "message": "Camera stopped"
    }

@image_router.get('/stream/{file}', response_class=FileResponse)
async def stream(
    file: str,
    token: str = ""
):
    if file.split(".")[-1] == "m3u8":
        user = get_current_user_from_token(token=token)
        return FileResponse(
            path=f"stream/{file}",
        )
    if file.split(".")[-1] == "ts":
        return FileResponse(
            path=f"stream/{file}",
        )
    
