from typing import Optional
from litestar import Litestar, get
from sqlalchemy import select

from src.routes.products import ProductController

@get('/')
async def hello() -> dict:
    return {"message": "Hello World"}

route_handlers = [
    hello,
    ProductController
]

app = Litestar(
    route_handlers=route_handlers,
)