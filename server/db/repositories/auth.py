from typing import List
from uuid import UUID, uuid4

from core.config import PWD_CONTEXT
from db.db import database, users
from db.errors import EntityDoesNotExist
from models.domain.auth import User
from models.schemas.auth import UserInCreate, UserInResponse, UserInUpdate


class UserRepository:
    """A repository class for working with Users in the database"""

    async def get_all_users(self) -> List[UserInResponse]:
        """Get all the tasks."""
        query = users.select()
        users_rows = await database.fetch_all(query=query)
        return [UserInResponse(**user) for user in users_rows]

    async def get_user_by_username(self, username: str) -> UserInResponse:
        """Get a single user by ID."""
        query = users.select().where(username == users.c.username)
        user_row = await database.fetch_one(query=query)

        if user_row:
            return UserInResponse(**user_row)

        raise EntityDoesNotExist("user with id {0} does not exist".format(id))

    async def get_user_by_id(self, id: UUID) -> UserInResponse:
        """Get a single user by ID."""
        query = users.select().where(id == users.c.id)
        user_row = await database.fetch_one(query=query)

        if user_row:
            return UserInResponse(**user_row)

        raise EntityDoesNotExist("user with id {0} does not exist".format(id))

    async def create_user(self, u: UserInCreate) -> UserInResponse:
        """Create a user in the database, then return it."""
        new_id = uuid4()
        query = users.insert().values(
            id=new_id,
            username=u.username,
            hashed_password=PWD_CONTEXT.hash(u.password),
            full_name=u.full_name,
            is_disabled=u.is_disabled,
        )
        await database.execute(query=query)
        return await self.get_user_by_id(new_id)

    async def update_task(self, id: UUID, u: UserInUpdate) -> UserInResponse:
        """Update a specific user"""
        query = (
            users.update()
            .where(id == users.c.id)
            .values(
                id=id,
                username=u.username,
                hashed_password=PWD_CONTEXT.hash(u.password),
                full_name=u.full_name,
                is_disabled=u.is_disabled,
            )
        )
        await database.execute(query=query)
        return await self.get_user_by_id(id)

    async def delete_user(self, id: UUID) -> None:
        """Delete a specific task"""
        query = users.delete().where(id == users.c.id)
        return await database.execute(query=query)
