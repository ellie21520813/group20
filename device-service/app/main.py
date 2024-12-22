from fastapi import FastAPI, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware

from app.api.v1.device import device_router
from app.api.v1.token import token_router
from app.api.v1.discover import discover_router
from app.api.v1.config import config_route
from app.service.ws import ws_router
from app.db.session import engine, database
from app.db.base_class import Base
from app.core.config import settings

# from app.service.mqtt_v2 import MQTTService

Base.metadata.create_all(bind=engine)
app = FastAPI(
    openapi_url=f"/api/{settings.VERSION}/device/openapi.json", 
    docs_url=f"/api/{settings.VERSION}/device/docs",
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"]
)


@app.on_event("startup")
async def startup():
    await database.connect()
    # t = BackgroundTasks()
    # t.start()

@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()

app.include_router(device_router, prefix=f"/api/{settings.VERSION}/device", tags=["Device"])
app.include_router(token_router, prefix=f"/api/{settings.VERSION}/device/token", tags=["Device Token"])
app.include_router(discover_router, prefix=f"/api/{settings.VERSION}/device/discover", tags=["Discover"])
app.include_router(config_route, prefix=f"/api/{settings.VERSION}/device/config", tags=["Device Config"])
app.include_router(ws_router, prefix=f'/ws/device', tags=["Websocket"])


from pyctuator.pyctuator import Pyctuator
from pyctuator.health.db_health_provider import DbHealthProvider
pyctuator = Pyctuator(
    app,
    "Device Service",
    app_url="http://device-service:8000",
    pyctuator_endpoint_url="http://device-service:8000/pyctuator",
    registration_url="http://localhost:8080/instances",
    app_description="Device management service",
    additional_app_info=dict(
        serviceLinks=dict(
            API_Docs="https://baonv.uitiot.vn/api/v1/device/docs"
        ),
    )
)
pyctuator.set_build_info(
    name="Device Service",
    version="1.0"
)
pyctuator.register_health_provider(DbHealthProvider(engine))
