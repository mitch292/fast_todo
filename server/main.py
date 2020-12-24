from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from api.routes.tasks import task_router
from core.config import DEBUG, PROJET_NAME, VERSION
from db.db import database

app = FastAPI(title=PROJET_NAME, debug=DEBUG, version=VERSION)

# FIXME
origins = [
    "http://localhost",
    "http://localhost:8000",
    "http://localhost:3000",
    "http://localhost:19006",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
async def startup():
    await database.connect()


@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()


app.include_router(task_router, prefix="/tasks", tags=["tasks"])
