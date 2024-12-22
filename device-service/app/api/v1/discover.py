import subprocess
import re

from fastapi import APIRouter, HTTPException, status, WebSocket
from fastapi import Depends
from fastapi.responses import HTMLResponse
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.core.config import settings
from app.deps.auth import get_current_user_from_token
from app.db.models.device import Device
from app.schemas.device import DeviceCreate, DeviceShow
from app.schemas.pagination import Pagination, PaginationShow
from app.schemas.pagination_res import PaginationResponse


discover_router = APIRouter()


def get_ip_esp8266():
    try:
        output = subprocess.check_output(["avahi-browse", "-ptr", "_arduino._tcp"]).decode('utf-8')
    except:
        return []

    outputs = output.split('\n')
    ips = re.findall(r'[0-9]+(?:\.[0-9]+){3}', output)
    res = []
    for o in outputs:
        for ip in ips:
            if ip in o:
                _tmp = o.split(';')[-1].replace('\"', '').split(" ")
                __tmp = []
                for i in _tmp:
                    __tmp.append(i.split('=')[-1])
                res.append(o.split(';')[6:-1] + __tmp)

    return res


@discover_router.get("/esp8266")
def scan_esp8266():
    return get_ip_esp8266()