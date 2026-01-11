from litestar import Litestar, get
from sqlalchemy import select

from src.db.models import ProductModel
from src.routes.products import ProductController
from src.routes.suppliers import SupplierController
from src.routes.purchase_orders import PurchaseOrderController
from src.db.setup import sqla_plugin, sqla_config

@get('/')
async def hello() -> dict:
    return {"message": "Hello World"}

route_handlers = [
    hello,
    ProductController,
    SupplierController,
    PurchaseOrderController
]


app = Litestar(
    route_handlers=route_handlers,
    plugins=[sqla_plugin]
)