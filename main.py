from litestar import Litestar, get
from sqlalchemy import select

from src.db.models import ProductModel
from src.routes.products import ProductController
from src.db.setup import sqla_plugin, sqla_config

@get('/')
async def hello() -> dict:
    return {"message": "Hello World"}

route_handlers = [
    hello,
    ProductController
]

async def init_db(app: Litestar) -> None:
    async with sqla_config.get_session() as session:
        statement = select(ProductModel).order_by(ProductModel.created_at.desc())
        result = await session.execute(statement)
        print(result.all())

app = Litestar(
    route_handlers=route_handlers,
    plugins=[sqla_plugin],
    on_startup=[init_db]
)