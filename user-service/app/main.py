from fastapi import FastAPI
from app.api.v1.users import user_router
from app.api.v1.role import role_router

from app.db.session import engine, database
from app.db.base_class import Base
from app.core.config import settings
from fastapi.middleware.cors import CORSMiddleware


Base.metadata.create_all(bind=engine)

app = FastAPI(
    openapi_url=f"/api/{settings.VERSION}/user/openapi.json", 
    docs_url=f"/api/{settings.VERSION}/user/docs"
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

app.include_router(user_router, prefix=f"/api/{settings.VERSION}/user", tags=["User"])
app.include_router(role_router, prefix=f"/api/{settings.VERSION}/role", tags=["Role"])


from pyctuator.pyctuator import Pyctuator
from pyctuator.health.db_health_provider import DbHealthProvider
pyctuator = Pyctuator(
    app,
    "User Service",
    app_url="http://user-service:8000",
    pyctuator_endpoint_url="http://user-service:8000/pyctuator",
    registration_url="http://spring-admin:8080/instances",
    app_description="User management service",
    additional_app_info=dict(
        serviceLinks=dict(
            API_Docs="https://baonv.uitiot.vn/api/v1/user/docs"
        ),
    )
)
pyctuator.set_build_info(
    name="User Service",
    version="1.0"
)
pyctuator.register_health_provider(DbHealthProvider(engine))
