from fastapi import FastAPI

from api.routes.tasks import task_router

app = FastAPI()

app.include_router(task_router,  prefix="/tasks", tags=["tasks"])