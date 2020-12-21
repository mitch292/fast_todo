from typing import Optional
from uuid import UUID

from pydantic import BaseModel

from models.domain.task import CategoryType, Task


class TaskInResponse(Task):
    pass


class TaskInCreate(BaseModel):
    description: str
    category: Optional[CategoryType]
    is_complete: Optional[bool] = False


class TaskInUpdate(Task):
    description: Optional[str]
    category: Optional[CategoryType]
    is_complete: Optional[bool]
    id: Optional[UUID]


class TaskInDelete(BaseModel):
    pass
