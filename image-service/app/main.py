from fastapi import FastAPI, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware

from app.api.v1.image import image_router
# from app.service.ws import ws_router
# from app.db.session import engine, database
# from app.db.base_class import Base
from app.core.config import settings


# Base.metadata.create_all(bind=engine)
app = FastAPI(
    openapi_url=f"/api/{settings.VERSION}/image/openapi.json", 
    docs_url=f"/api/{settings.VERSION}/image/docs",
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"]
)


@app.on_event("startup")
async def startup():
    # await database.connect()
    pass

@app.on_event("shutdown")
async def shutdown():
    # await database.disconnect()
    pass

app.include_router(image_router, prefix=f"/api/{settings.VERSION}/camera", tags=["Image"])

# from pyctuator.pyctuator import Pyctuator
# from pyctuator.health.db_health_provider import DbHealthProvider
# pyctuator = Pyctuator(
#     app,
#     "Image Service",
#     app_url="http://image-service:8000",
#     pyctuator_endpoint_url="http://image-service:8000/pyctuator",
#     registration_url="http://spring-admin:8080/instances",
#     app_description="Image service",
#     additional_app_info=dict(
#         serviceLinks=dict(
#             API_Docs="https://baonv.uitiot.vn/api/v1/image/docs"
#         ),
#     )
# )
# pyctuator.set_build_info(
#     name="Image Service",
#     version="1.0"
# )
# pyctuator.register_health_provider(DbHealthProvider(engine))
