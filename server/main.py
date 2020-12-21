from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from api.routes.tasks import task_router
from core.config import DEBUG, PROJET_NAME, VERSION
from core.events import create_start_app_handler, create_stop_app_handler

app = FastAPI(title=PROJET_NAME, debug=DEBUG, version=VERSION)

origins = [
    "http://localhost",
    "http://localhost:8000",
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.add_event_handler("startup", create_start_app_handler(app))
app.add_event_handler("shutdown", create_stop_app_handler(app))

app.include_router(task_router, prefix="/tasks", tags=["tasks"])
