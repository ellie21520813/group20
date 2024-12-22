from fastapi import FastAPI
from app.db.session import engine, database
from app.db.base_class import Base
from app.core.config import settings
from fastapi.middleware.cors import CORSMiddleware

from app.api.v1.file import file_router

Base.metadata.create_all(bind=engine)

app = FastAPI(
    openapi_url=f"/api/{settings.VERSION}/file/openapi.json", 
    docs_url=f"/api/{settings.VERSION}/file/docs"
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


@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()

app.include_router(file_router, prefix=f"/api/{settings.VERSION}/file", tags=["File"])


from pyctuator.pyctuator import Pyctuator
from pyctuator.health.db_health_provider import DbHealthProvider
pyctuator = Pyctuator(
    app,
    "File Service",
    app_url="http://file-service:8000",
    pyctuator_endpoint_url="http://file-service:8000/pyctuator",
    registration_url="http://spring-admin:8080/instances",
    app_description="File management service",
    additional_app_info=dict(
        serviceLinks=dict(
            API_Docs="https://baonv.uitiot.vn/api/v1/file/docs"
        ),
    )
)
pyctuator.set_build_info(
    name="File Service",
    version="1.0"
)
pyctuator.register_health_provider(DbHealthProvider(engine))
