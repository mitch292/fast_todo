import sqlalchemy
import databases
from uuid import UUID

from core.config import DATABASE_URL
database = databases.Database(DATABASE_URL)

# FIXME: This will eventually become a migration
metadata = sqlalchemy.MetaData()

tasks = sqlalchemy.Table(
    "tasks",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.String, primary_key=True),
    sqlalchemy.Column("description", sqlalchemy.String),
    sqlalchemy.Column("category", sqlalchemy.String),
    sqlalchemy.Column("is_complete", sqlalchemy.Boolean),
)

engine = sqlalchemy.create_engine(
    DATABASE_URL, connect_args={"check_same_thread": False}
)
metadata.create_all(engine)

# END FIXME

async def connect_to_db() -> None:
    await database.connect()

async def close_db_connection() -> None:
    await database.disconnect()