from typing import List
from uuid import UUID

from fastapi import APIRouter, Depends, status

from db.repositories.tasks import TasksRepository
from models.schemas.task import TaskInCreate, TaskInDelete, TaskInResponse, TaskInUpdate

router = APIRouter()


@router.get(
    "/",
    status_code=status.HTTP_200_OK,
    response_description="List all of the tasks.",
    response_model=List[TaskInResponse],
)
async def list_tasks(
    tasks_repo=Depends(TasksRepository),
) -> List[TaskInResponse]:
    return await tasks_repo.get_all_tasks()


@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_task(task: TaskInCreate, tasks_repo=Depends(TasksRepository)):
    return await tasks_repo.create_task(task)


@router.get(
    "/{id}/", response_description="Get a single task.", response_model=TaskInResponse
)
async def get_task(id: UUID, tasks_repo=Depends(TasksRepository)) -> TaskInResponse:
    return await tasks_repo.get_task_by_id(id)


@router.put("/{id}/", response_model=TaskInResponse)
async def update_task(
    id: UUID, task: TaskInUpdate, tasks_repo=Depends(TasksRepository)
):
    return await tasks_repo.update_task(id, task)


@router.delete("/{id}/", response_model=TaskInDelete)
async def delete_task(id: UUID, tasks_repo=Depends(TasksRepository)):
    return await tasks_repo.delete_task(id)
