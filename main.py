from litestar import Litestar, get

from src.db.setup import sqla_plugin
from src.routes.products import ProductController
from src.routes.purchase_orders import PurchaseOrderController
from src.routes.supplier_invoices import SupplierInvoiceController
from src.routes.suppliers import SupplierController


@get("/")
async def hello() -> dict:
    return {"message": "Hello World"}


route_handlers = [
    hello,
    ProductController,
    SupplierController,
    PurchaseOrderController,
    SupplierInvoiceController,
]


app = Litestar(route_handlers=route_handlers, plugins=[sqla_plugin])
