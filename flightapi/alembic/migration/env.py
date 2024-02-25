import logging
import os
import re
import sys
from logging.config import fileConfig

from alembic import context
from sqlalchemy import engine_from_config, pool, create_engine

from flightapi.db_config import DATABASE_URL
from flightapi.models import Base

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)

logger = logging.getLogger("alembic.env")

# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config

# Interpret the config file for Python logging.
# This line sets up loggers basically.
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# Register models within the environment
# Will not pick up models if import statements are not present

# add your model's MetaData object here
# for 'autogenerate' support
# from myapp import mymodel
# target_metadata = mymodel.Base.metadata

target_metadata = Base.metadata

# Exclude postgis extension tables as Alembic will think we are wanting
# to delete these following the initial migration - since we have no metadata targets for these tables

IGNORE_TABLES = ["spatial_ref_sys", "us_gaz", "us_lex", "us_rules", "layer", "topology"]


def include_object(object, name, type_, reflected, compare_to):
    if type_ == "table" and (
        name in IGNORE_TABLES or object.info.get("skip_autogenerate", False)
    ):
        return False

    elif type_ == "column" and object.info.get("skip_autogenerate", False):
        return False

    return True


# other values from the config, defined by the needs of env.py,
# can be acquired:
# my_important_option = config.get_main_option("my_important_option")
# ... etc.


def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode.

    This configures the context with just a URL
    and not an Engine, though an Engine is acceptable
    here as well.  By skipping the Engine creation
    we don't even need a DBAPI to be available.

    Calls to context.execute() here emit the given string to the
    script output.

    """
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
        include_object=include_object,
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """Run migrations in 'online' mode.

    In this scenario we need to create an Engine
    and associate a connection with the context.

    """
    if config.get_main_option("is_testing", "False") == "True":
        url = config.get_main_option("sqlalchemy.url")
    else:
        url = DATABASE_URL

    # Output the DB URL to ensure we're reflecting the proper one for main and testing
    print("URL=" + str(url))
    connectable = create_engine(url)
    # connectable = engine_from_config(
    #     config.get_section(config.config_ini_section, {}),
    #     prefix="sqlalchemy.",
    #     poolclass=pool.NullPool,
    # )

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
            compare_server_default=True,
            include_object=include_object,
            compare_type=True,
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    logger.info("Running migrations offline mode")
    run_migrations_offline()
else:
    logger.info("Running migrations online mode")
    run_migrations_online()
