from fastapi import FastAPI
from app.db.session import engine, database
from app.db.base_class import Base
from app.core.config import settings
from fastapi.middleware.cors import CORSMiddleware

from app.api.v1.task import task_router

Base.metadata.create_all(bind=engine)

app = FastAPI(
    openapi_url=f"/api/{settings.VERSION}/task/openapi.json", 
    docs_url=f"/api/{settings.VERSION}/task/docs"
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

app.include_router(task_router, prefix=f"/api/{settings.VERSION}/task", tags=["Task"])


from pyctuator.pyctuator import Pyctuator
from pyctuator.health.db_health_provider import DbHealthProvider
pyctuator = Pyctuator(
    app,
    "Task Service",
    app_url="http://task-service:8000",
    pyctuator_endpoint_url="http://task-service:8000/pyctuator",
    registration_url="http://spring-admin:8080/instances",
    app_description="Task management service",
    additional_app_info=dict(
        serviceLinks=dict(
            API_Docs="https://baonv.uitiot.vn/api/v1/task/docs"
        ),
    )
)
pyctuator.set_build_info(
    name="Task Service",
    version="1.0"
)
pyctuator.register_health_provider(DbHealthProvider(engine))
