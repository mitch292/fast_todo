from typing import List
from uuid import uuid4

from fastapi import APIRouter, Request

from models.schemas.task import TaskInResponse
from models.domain.task import Task

task_router = APIRouter() 

@task_router.get('/', status_code=200, response_description="List all of the tasks", response_model=List[TaskInResponse])
async def list_tasks(request: Request) -> List[TaskInResponse] :
    return [
        Task(id=uuid4(), is_complete=False, description="test123", category="vanilla")
    ]