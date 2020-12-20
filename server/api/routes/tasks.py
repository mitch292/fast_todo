from typing import List
from uuid import UUID, uuid4

from fastapi import APIRouter, Request, Depends

from models.schemas.task import TaskInResponse, TaskInCreate, TaskInUpdate, TaskInDelete
from models.domain.task import Task
from .dependencies.database import get_repository
from db.repositories.tasks import TasksRepository

task_router = APIRouter() 

@task_router.get('/', status_code=200, response_description="List all of the tasks.", response_model=List[TaskInResponse])
async def list_tasks(tasks_repo = Depends(get_repository(TasksRepository))) -> List[TaskInResponse]:
    return await tasks_repo.get_all_tasks()

@task_router.post('/', status_code=201)
async def create_task(task: TaskInCreate):
    return {"created": "okay"}

@task_router.get('/{id}', response_description="Get a single task.", response_model=TaskInResponse)
async def get_task(id: UUID) -> TaskInResponse: 
    return Task(id=uuid4(), is_complete=True, description="A single task", category="the_worst")

@task_router.put('/{id}', response_model=TaskInUpdate)
async def update_task(id: UUID):
    return {"updated": "okay"}

@task_router.delete('/{id}', response_model=TaskInDelete)
async def delete_task(id: UUID):
    return {"deleted": "okay"}