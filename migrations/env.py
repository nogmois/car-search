from logging.config import fileConfig
from sqlalchemy import engine_from_config, pool
from alembic import context

# +++ Início das adições +++
from dotenv import load_dotenv
import os

# Carrega variáveis do .env
load_dotenv()
# Sobrescreve a URL do alembic.ini com a do .env
config = context.config
config.set_main_option('sqlalchemy.url', os.getenv('DATABASE_URL'))

# Importa seu metadata
from app.models import Base
target_metadata = Base.metadata
# +++ Fim das adições +++


def run_migrations_offline() -> None:
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )
    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    connectable = engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection, target_metadata=target_metadata
        )
        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
