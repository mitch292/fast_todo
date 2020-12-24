from typing import List
from uuid import UUID, uuid4

from db.db import database, tasks
from db.errors import EntityDoesNotExist
from models.domain.task import Task
from models.schemas.task import TaskInCreate, TaskInUpdate


class TasksRepository:
    """A repository class for working with Tasks in the database"""

    async def get_all_tasks(self) -> List[Task]:
        """Get all the tasks."""
        query = tasks.select()
        tasks_row = await database.fetch_all(query=query)
        return [Task(**task) for task in tasks_row]

    async def get_task_by_id(self, id: UUID) -> Task:
        """Get a single task by ID."""
        query = tasks.select().where(id == tasks.c.id)
        task_row = await database.fetch_one(query=query)

        if task_row:
            return Task(**task_row)

        raise EntityDoesNotExist("task with id {0} does not exist".format(id))

    async def create_task(self, t: TaskInCreate) -> Task:
        """Create a task in the database, then return it."""
        new_id = uuid4()
        query = tasks.insert().values(
            id=new_id,
            description=t.description,
            category=t.category,
            is_complete=t.is_complete,
        )
        # FIXME: We should need to execute two queries here
        await database.execute(query=query)
        return await self.get_task_by_id(new_id)

    async def update_task(self, id: UUID, t: TaskInUpdate) -> Task:
        """Update a specific task"""
        query = (
            tasks.update()
            .where(id == tasks.c.id)
            .values(
                description=t.description,
                category=t.category,
                is_complete=t.is_complete,
            )
        )
        await database.execute(query=query)
        return await self.get_task_by_id(id)

    async def delete_task(self, id: UUID) -> None:
        """Delete a specific task"""
        query = tasks.delete().where(id == tasks.c.id)
        return await database.execute(query=query)
