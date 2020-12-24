from typing import List
from uuid import UUID, uuid4

from core.config import PWD_CONTEXT
from db.db import database, users
from db.errors import EntityDoesNotExist
from models.domain.auth import User
from models.schemas.auth import UserInCreate, UserInDB, UserInUpdate


class UserRepository:
    """A repository class for working with Users in the database"""

    async def get_all_users(self) -> List[UserInDB]:
        """Get all the tasks."""
        query = users.select()
        users_rows = await database.fetch_all(query=query)
        print('the users rows', users_rows[0].__dict__)
        return [UserInDB(**user) for user in users_rows]

    async def get_user_by_id(self, id: UUID) -> UserInDB:
        """Get a single user by ID."""
        query = users.select().where(id == users.c.id)
        user_row = await database.fetch_one(query=query)

        if user_row:
            print('the user row', dict(user_row))
            return UserInDB(**user_row)

        raise EntityDoesNotExist("user with id {0} does not exist".format(id))

    async def create_user(self, u: UserInCreate) -> UserInDB:
        """Create a user in the database, then return it."""
        new_id = uuid4()
        query = users.insert().values(
            id=new_id,
            username=u.username,
            hashed_password=PWD_CONTEXT.hash(u.password),
            full_name=u.full_name,
            is_disabled=u.is_disabled,
        )
        # FIXME: We should need to execute two queries here
        await database.execute(query=query)
        return await self.get_user_by_id(new_id)

    async def update_task(self, id: UUID, u: UserInUpdate) -> UserInDB:
        """Update a specific user"""
        query = (
            users.update()
            .where(id == users.c.id)
            .values(
                id=new_id,
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
