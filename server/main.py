from fastapi import FastAPI

from api.routes.tasks import task_router
from core.events import create_start_app_handler, create_stop_app_handler
from core.config import PROJET_NAME, DEBUG, VERSION

app = FastAPI(title=PROJET_NAME, debug=DEBUG, version=VERSION)

app.add_event_handler("startup", create_start_app_handler(app))
app.add_event_handler("shutdown", create_stop_app_handler(app))

app.include_router(task_router,  prefix="/tasks", tags=["tasks"])