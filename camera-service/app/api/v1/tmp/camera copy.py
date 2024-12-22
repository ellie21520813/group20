import cv2
import io
import threading
import time
import imutils
import os

from fastapi import APIRouter, HTTPException, status, WebSocket
from fastapi import Depends
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

camera_router = APIRouter()

manager = None
count_keep_alive = 0
stop_streaming = False
os.environ["OPENCV_FFMPEG_CAPTURE_OPTIONS"] = "rtsp_transport;udp"

def start_stream(url_rtsp, manager):
    global width
    global height

    vs = VideoStream(url_rtsp).start()
    while True:
        # time.sleep(0.2)
        frame = vs.read()
        # frame = imutils.resize(frame, width=680)
        output_frame = frame.copy()

        if output_frame is None:
            continue
        (flag, encodedImage) = cv2.imencode(".jpg", output_frame)
        if not flag:
            continue
        manager.put(encodedImage)


def streamer():
    try:
        while manager:
            yield (b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n' +
                   bytearray(manager.get()) + b'\r\n')
    except GeneratorExit:
        print("cancelled")


def manager_keep_alive(p):
    global count_keep_alive
    global manager
    global stop_streaming
    while count_keep_alive > 0 and not stop_streaming:
        time.sleep(1)
        print(count_keep_alive)
        count_keep_alive -= 1
    p.kill()
    time.sleep(.5)
    p.close()
    manager.close()
    manager = None
    print("Stop streaming")

@camera_router.get("/stream")
async def stream():
    return StreamingResponse(streamer(), media_type="multipart/x-mixed-replace;boundary=frame")

@camera_router.get("/stop")
async def stop_video_streaming():
    global stop_streaming
    stop_streaming = True

@camera_router.post("/keep-alive")
def keep_alive(
    camera: Camera,
    user = Depends(get_current_user_from_token)
):
    if user['username'] != camera.owner:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="You are not permitted!"
        )
    if camera.username != "":
        stream_url = f"{camera.protocol}://{camera.username}:{camera.password}@{camera.ip}:{camera.port}{camera.path}"
    else:
        stream_url = f"{camera.protocol}://{camera.ip}:{camera.port}{camera.path}"

    global manager
    global count_keep_alive
    global stop_streaming
    stop_streaming = False
    count_keep_alive = 60
    if not manager:
        manager = Queue()
        p = Process(target=start_stream, args=(stream_url, manager,))
        p.start()
        threading.Thread(target=manager_keep_alive, args=(p,)).start()
    return "http://192.168.31.76/api/v1/camera/stream"

@camera_router.post('/capture', response_class=FileResponse)
async def capture(
    camera: Camera,
    user = Depends(get_current_user_from_token)
):
    if user['username'] != camera.owner:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="You are not permitted!"
        )
    
    if camera.username != "":
        stream_url = f"{camera.protocol}://{camera.username}:{camera.password}@{camera.ip}:{camera.port}{camera.path}"
    else:
        stream_url = f"{camera.protocol}://{camera.ip}:{camera.port}{camera.path}"

    capture = cv2.VideoCapture(stream_url, cv2.CAP_FFMPEG)
    ret, img = capture.read()
    res, im_png = cv2.imencode(".png", img)
    return StreamingResponse(io.BytesIO(im_png.tobytes()), media_type="image/png")
    