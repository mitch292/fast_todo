"""create tasks table

Revision ID: e97ea08403f5
Revises: 
Create Date: 2020-12-20 13:17:10.469225

"""
from typing import Tuple
import uuid
from alembic import op
import sqlalchemy as sa
from sqlalchemy import func
from sqlalchemy.dialects.postgresql import UUID


# revision identifiers, used by Alembic.
revision = 'e97ea08403f5'
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

def create_tasks_table() -> None:
    op.create_table(
        "tasks",
        sa.Column("id", UUID(as_uuid=True), primary_key=True, default=lambda: uuid.uuid4().hex, unique=True),
        sa.Column("description", sa.String),
        sa.Column("category", sa.String),
        sa.Column("is_complete", sa.Boolean),
        *timestamps(),
    )


def upgrade():
    create_updated_at_trigger()
    create_tasks_table()


def downgrade():
    op.drop_table("tasks")
    op.execute("DROP FUNCTION update_updated_at_column")
