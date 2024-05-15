import asyncio
import os
from logging.config import fileConfig

import sqlalchemy.schema
from alembic import context
from sqlalchemy.sql.ddl import CreateSchema

from ..config import settings
from ..models import Base
from asyncpg import Connection
from sqlalchemy import pool
from sqlalchemy.ext.asyncio import async_engine_from_config

# from main_app_service.app.database import Base

# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config

# Interpret the config file for Python logging.
# This line sets up loggers basically.
fileConfig(config.config_file_name)  # type: ignore

# add your model's MetaData object here
target_metadata = Base.metadata


# def get_url():
#     return os.getenv("DATABASE_URL")


def run_migrations_offline():
    """Run migrations in 'offline' mode.
    This configures the context with just a URL
    and not an Engine, though an Engine is acceptable
    here as well.  By skipping the Engine creation
    we don't even need a DBAPI to be available.
    Calls to context.execute() here emit the given string to the
    script output.
    """
    # url = config.get_main_option("sqlalchemy.url")
    url = settings.database_url_asyncpg()
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def do_run_migrations(connection: Connection) -> None:
    """
            Configure migration context
            1. Pass our models metadata
            2. Set schema for alembic_version table
            3. Load all available schemas
            """
    context.configure(connection=connection, target_metadata=target_metadata,
                      version_table_schema=target_metadata.schema,
                      include_schemas=True)

    with context.begin_transaction():
        # context.execute(f'CREATE SCHEMA IF NOT EXISTS {settings.DB_SCHEMA}')
        context.execute(f'SET search_path TO public')
        context.run_migrations()


async def run_migrations_online():
    """Run migrations in 'online' mode.
    In this scenario we need to create an Engine
    and associate a connection with the context.
    """
    configuration = config.get_section(config.config_ini_section)
    configuration["sqlalchemy.url"] = settings.database_url_asyncpg
    connectable = async_engine_from_config(
        configuration,
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    async with connectable.connect() as connection:
        await connection.run_sync(do_run_migrations)
    await connectable.dispose()


if context.is_offline_mode():
    run_migrations_offline()
else:
    asyncio.run(run_migrations_online())
