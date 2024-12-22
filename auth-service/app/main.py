from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.v1.login import login_router
from app.db.session import engine, database
from app.db.base_class import Base
from app.core.config import settings

Base.metadata.create_all(bind=engine)

app = FastAPI(
    openapi_url=f"/api/{settings.VERSION}/auth/openapi.json", 
    docs_url=f"/api/{settings.VERSION}/auth/docs"
)

origins = [
    "http://localhost",
    "http://localhost:3000",
    "http://localhost:8888",
    "http://172.31.10.112:3000"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_methods=["*"],
    allow_headers=["*"]
)

@app.on_event("startup")
async def startup():
    await database.connect()


@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()


app.include_router(login_router, prefix=f"/api/{settings.VERSION}/auth", tags=["Authentication"])

from pyctuator.pyctuator import Pyctuator
from pyctuator.health.db_health_provider import DbHealthProvider
pyctuator = Pyctuator(
    app,
    "Auth Service",
    app_url="http://auth-service:8000",
    pyctuator_endpoint_url="http://auth-service:8000/pyctuator",
    registration_url="http://spring-admin:8080/instances",
    app_description="Auth management service",
    additional_app_info=dict(
        serviceLinks=dict(
            API_Docs="https://baonv.uitiot.vn/api/v1/auth/docs"
        ),
    )
)
pyctuator.set_build_info(
    name="Auth Service",
    version="1.0"
)
pyctuator.register_health_provider(DbHealthProvider(engine))
