"""create initial tables

Revision ID: e97ea08403f5
Revises:
Create Date: 2020-12-20 13:17:10.469225

"""
from typing import Tuple
from uuid import uuid4

import sqlalchemy as sa
from alembic import op
from sqlalchemy import func
from sqlalchemy.dialects.postgresql import UUID

# revision identifiers, used by Alembic.
revision = "e97ea08403f5"
down_revision = None
branch_labels = None
depends_on = None


def create_updated_at_trigger() -> None:
    op.execute(
        """
    CREATE FUNCTION update_updated_at_column()
        RETURNS TRIGGER AS
    $$
    BEGIN
        NEW.updated_at = now();
        RETURN NEW;
    END;
    $$ language 'plpgsql';
    """
    )


def timestamps() -> Tuple[sa.Column, sa.Column]:
    return (
        sa.Column(
            "created_at",
            sa.TIMESTAMP(timezone=True),
            nullable=False,
            server_default=func.now(),
        ),
        sa.Column(
            "updated_at",
            sa.TIMESTAMP(timezone=True),
            nullable=False,
            server_default=func.now(),
        ),
    )


def create_users_table() -> None:
    op.create_table(
        "users",
        sa.Column(
            "id",
            UUID,
            primary_key=True,
            default=uuid4,
            unique=True,
        ),
        sa.Column("username", sa.String, unique=True, nullable=False, index=True),
        sa.Column("hashed_password", sa.String),
        sa.Column("full_name", sa.String, nullable=True, server_default=""),
        sa.Column("is_disabled", sa.Boolean),
        *timestamps(),
    )


def create_tasks_table() -> None:
    op.create_table(
        "tasks",
        sa.Column(
            "id",
            UUID,
            primary_key=True,
            default=uuid4,
            unique=True,
        ),
        sa.Column("description", sa.String),
        sa.Column("category", sa.String),
        sa.Column("is_complete", sa.Boolean),
        sa.Column("user_id", UUID, sa.ForeignKey("users.id")),
        *timestamps(),
    )


def upgrade():
    create_updated_at_trigger()
    create_users_table()
    create_tasks_table()


def downgrade():
    op.drop_table("tasks")
    op.drop_table("users")
    op.execute("DROP FUNCTION update_updated_at_column")
