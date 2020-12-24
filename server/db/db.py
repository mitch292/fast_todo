from uuid import uuid4

from databases import Database
from sqlalchemy import (TIMESTAMP, Boolean, Column, Integer, MetaData, String,
                        Table, create_engine)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func

from core.config import DATABASE_URL

# SQLAlchemy
engine = create_engine(str(DATABASE_URL))
metadata = MetaData()
tasks = Table(
    "tasks",
    metadata,
    Column(
        "id",
        UUID(as_uuid=True),
        primary_key=True,
        default=lambda: uuid4().hex,
        unique=True,
    ),
    Column("id", Integer, primary_key=True),
    Column("description", String),
    Column("category", String),
    Column("is_complete", Boolean),
    Column(
        "created_at",
        TIMESTAMP(timezone=True),
        server_default=func.now(),
        nullable=False,
    ),
    Column(
        "updated_at",
        TIMESTAMP(timezone=True),
        server_default=func.now(),
        nullable=False,
        onupdate=func.now(),
    ),
)

# databases query builder
database = Database(str(DATABASE_URL))
