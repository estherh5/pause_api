import os
from logging.config import fileConfig

from sqlalchemy import engine_from_config, pool

from alembic import context
from pause import models

config = context.config

if config.config_file_name:
    fileConfig(config.config_file_name)

database_url = os.getenv("DB_CONNECTION", os.getenv("DATABASE_URL"))
if not database_url:
    raise RuntimeError("DB_CONNECTION or DATABASE_URL must be set")

config.set_main_option("sqlalchemy.url", database_url.replace("%", "%%"))
target_metadata = models.Base.metadata


def run_migrations_offline():
    context.configure(
        url=database_url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online():
    connectable = engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
