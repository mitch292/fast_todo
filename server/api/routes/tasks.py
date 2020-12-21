from typing import List
from uuid import UUID

from fastapi import APIRouter, Depends

from db.repositories.tasks import TasksRepository
from models.schemas.task import (TaskInCreate, TaskInDelete, TaskInResponse,
                                 TaskInUpdate)

from .dependencies.database import get_repository

task_router = APIRouter()


@task_router.get(
    "/",
    status_code=200,
    response_description="List all of the tasks.",
    response_model=List[TaskInResponse],
)
async def list_tasks(
    tasks_repo=Depends(get_repository(TasksRepository)),
) -> List[TaskInResponse]:
    return await tasks_repo.get_all_tasks()


@task_router.post("/", status_code=201)
async def create_task(
    task: TaskInCreate, tasks_repo=Depends(get_repository(TasksRepository))
):
    return await tasks_repo.create_task(task)


@task_router.get(
    "/{id}", response_description="Get a single task.", response_model=TaskInResponse
)
async def get_task(
    id: UUID, tasks_repo=Depends(get_repository(TasksRepository))
) -> TaskInResponse:
    return await tasks_repo.get_task_by_id(id)


@task_router.put("/{id}", response_model=TaskInResponse)
async def update_task(
    id: UUID, task: TaskInUpdate, tasks_repo=Depends(get_repository(TasksRepository))
):
    return await tasks_repo.update_task(id, task)


@task_router.delete("/{id}", response_model=TaskInDelete)
async def delete_task(id: UUID, tasks_repo=Depends(get_repository(TasksRepository))):
    return await tasks_repo.delete_task(id)
