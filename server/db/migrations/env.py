import pathlib
import sys
from logging.config import fileConfig

from alembic import context
from sqlalchemy import engine_from_config, pool

from core.config import DATABASE_URL

sys.path.append(str(pathlib.Path(__file__).resolve().parents[2]))


config = context.config

fileConfig(config.config_file_name)

target_metadata = None
config.set_main_option("sqlalchemy.url", str(DATABASE_URL))


def run_migrations_online() -> None:
    print(config.get_section(config.config_ini_section))
    connectable = engine_from_config(
        config.get_section(config.config_ini_section),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(connection=connection, target_metadata=target_metadata)

        with context.begin_transaction():
            context.run_migrations()


run_migrations_online()
