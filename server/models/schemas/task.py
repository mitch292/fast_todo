from typing import Optional

from pydantic import BaseModel

from models.domain.task import CategoryType, Task


class TaskInResponse(Task):
    pass


class BaseTask(BaseModel):
    description: str
    category: Optional[CategoryType]
    is_complete: Optional[bool] = False


class TaskInCreate(BaseTask):
    pass


class TaskInUpdate(BaseTask):
    pass


class TaskInDelete(BaseModel):
    pass
