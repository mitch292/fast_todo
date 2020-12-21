from typing import Optional

from pydantic import BaseModel

from models.domain.task import CategoryType, Task


class TaskInResponse(Task):
    pass


class TaskInCreate(BaseModel):
    description: str
    category: Optional[CategoryType]
    is_complete: Optional[bool] = False


class TaskInUpdate(Task):
    pass


class TaskInDelete(BaseModel):
    pass
