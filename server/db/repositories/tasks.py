from typing import List
from uuid import UUID, uuid4

from db.db import database, tasks
from db.errors import EntityDoesNotExist
from models.domain.task import Task
from models.schemas.task import TaskInCreate, TaskInUpdate


class TasksRepository:
    """A repository class for working with Tasks in the database"""

    async def get_all_tasks(self, user_id: UUID) -> List[Task]:
        """Get all the tasks."""
        query = tasks.select().where(user_id == tasks.c.user_id)
        tasks_row = await database.fetch_all(query=query)
        return [Task(**task) for task in tasks_row]

    async def get_task_by_id(self, id: UUID, user_id: UUID) -> Task:
        """Get a single task by ID."""
        query = tasks.select().where(id == tasks.c.id).where(user_id == tasks.c.user_id)
        task_row = await database.fetch_one(query=query)

        if task_row:
            return Task(**task_row)

        raise EntityDoesNotExist("task with id {0} does not exist".format(id))

    async def create_task(self, t: TaskInCreate, user_id: UUID) -> Task:
        """Create a task in the database, then return it."""
        new_id = uuid4()
        query = tasks.insert().values(
            id=new_id,
            description=t.description,
            category=t.category,
            is_complete=t.is_complete,
            user_id=user_id,
        )
        # FIXME: We should need to execute two queries here
        await database.execute(query=query)
        return await self.get_task_by_id(new_id, user_id)

    async def update_task(self, id: UUID, t: TaskInUpdate, user_id: UUID) -> Task:
        """Update a specific task"""
        query = (
            tasks.update()
            .where(id == tasks.c.id)
            .where(user_id == tasks.c.user_id)
            .values(
                description=t.description,
                category=t.category,
                is_complete=t.is_complete,
            )
        )
        await database.execute(query=query)
        return await self.get_task_by_id(id, user_id)

    async def delete_task(self, id: UUID, user_id: UUID) -> None:
        """Delete a specific task"""
        query = tasks.delete().where(id == tasks.c.id).where(user_id == tasks.c.user_id)
        return await database.execute(query=query)
