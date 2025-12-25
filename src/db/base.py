from litestar.plugins.sqlalchemy import (
    SQLAlchemyInitPlugin, 
    SQLAlchemyAsyncConfig,
    AsyncSessionConfig,
)
from src.config import Config

#session 
sqla_session_config = AsyncSessionConfig(expire_on_commit=False)

# sqlalchemy config
sqla_config = SQLAlchemyAsyncConfig(
    connection_string=Config.DB_URL, 
    create_all=True, 
    session_config=sqla_session_config
)

sqla_plugin = SQLAlchemyInitPlugin(config=sqla_config)

# sqlalchemy.orm.DeclarativeBase
# litestar.plugins.sqlalchemy.base.BigIntBase (int primary key)
# litestar.plugins.sqlalchemy.base.BigIntAuditBase (int primary key + audit keys)
# litestar.plugins.sqlalchemy.base.UUIDBase (UUID primary key)
# litestar.plugins.sqlalchemy.base.UUIDAuditBased (int primary key + audit keys)


