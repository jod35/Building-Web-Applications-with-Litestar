from typing import Optional
from litestar import Litestar, get

from src.routes.products import ProductController
from src.db.base import sqla_plugin

@get('/')
async def hello() -> dict:
    return {"message": "Hello World"}

route_handlers = [
    hello,
    ProductController
]

app = Litestar(
    route_handlers=route_handlers,
    plugins=[sqla_plugin]
)