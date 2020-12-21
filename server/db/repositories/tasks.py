from typing import List
from uuid import UUID, uuid4

from db.errors import EntityDoesNotExist
from db.queries.qeuries import queries
from db.repositories.base import BaseRepository
from models.domain.task import Task
from models.schemas.task import TaskInCreate, TaskInUpdate


class TasksRepository(BaseRepository):
    async def get_all_tasks(self) -> List[Task]:
        tasks_row = await queries.get_all_tasks(self.connection)
        return [Task(**task) for task in tasks_row]

    async def get_task_by_id(self, id: UUID) -> Task:
        task_row = await queries.get_task_by_id(self.connection, id=id)

        if task_row:
            return Task(**task_row)

        raise EntityDoesNotExist("task with id {0} does not exist".format(id))

    async def create_task(self, t: TaskInCreate) -> Task:
        async with self.connection.transaction():
            task_row = await queries.create_new_task(
                self.connection,
                # asyncpg blocks us from leveraging the uuidv4
                # function we have defined on the model, so make it here instead
                id=uuid4(),
                description=t.description,
                category=t.category,
                is_complete=t.is_complete,
            )

            return Task(**task_row)

    async def update_task(self, id: UUID, t: TaskInUpdate) -> Task:
        async with self.connection.transaction():
            task_row = await queries.update_task_by_id(
                self.connection,
                id=id,
                description=t.description,
                category=t.category,
                is_complete=t.is_complete,
            )

            return Task(**task_row)

    async def delete_task(self, id: UUID) -> None:
        async with self.connection.transaction():
            await queries.delete_task_by_id(self.connection, id=id)
