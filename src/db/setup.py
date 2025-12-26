from litestar.plugins.sqlalchemy import (
    AsyncSessionConfig,
    SQLAlchemyAsyncConfig,
    SQLAlchemyInitPlugin,
)

from src.config import CONFIG

session_config = AsyncSessionConfig(expire_on_commit=False)

sqla_config = SQLAlchemyAsyncConfig(
    connection_string=CONFIG.DB_URL, session_config=session_config, create_all=True
)

sqla_plugin = SQLAlchemyInitPlugin(config=sqla_config)
