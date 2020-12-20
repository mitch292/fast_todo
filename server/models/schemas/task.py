from typing import Optional

from pydantic import BaseModel

from models.domain.task import Task

class TaskInResponse(Task):
    pass

class TaskInCreate(BaseModel):
    description: str
    category: Optional[str]
    is_complete: Optional[bool] = False