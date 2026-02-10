from typing import Any
from litestar import Litestar, get, Controller, Router
from litestar.di import Provide

from src.db.setup import sqla_plugin
from src.routes.products import ProductController
from src.routes.purchase_orders import PurchaseOrderController
from src.routes.supplier_invoices import SupplierInvoiceController
from src.routes.suppliers import SupplierController


async def provide_route_dependency() -> str:
    return "route dependency"

# __call__

async def provide_controller_dependency() -> str:
    return "controller dependency"


async def provide_router_dependency() -> str:
    return "router dependency"


async def provide_global_dependency() -> str:
    return "app dependency"


@get("/", dependencies={"route_dep": Provide(provide_route_dependency)})
async def hello(global_dep: str, route_dep: str) -> dict:
    return {"message": "Hello World", "route_dep": route_dep, "app_dep": global_dep}


class DummyController(Controller):
    dependencies = {"controller_dep": Provide(provide_controller_dependency)}

    @get("/dummy")
    async def dummy_list_obj(
        self, global_dep: str, controller_dep: str
    ) -> dict[str, Any]:
        return {
            "data": [{"id": 1}],
            "controller_dep": controller_dep,
            "app_dep": global_dep,
        }


@get(
    "/audit",
)
async def get_audit_trail(global_dep: str, router_dep: str) -> dict:
    return {
        "data": ["Audit trail entry 1", "Audit trail entry 2", "Audit trail entry 3"],
        "router_dep": router_dep,
        "app_dep": global_dep,
    }


class PaymentController(Controller):

    @get("/")
    async def list_all_payments(self, global_dep: str, router_dep: str) -> list:
        return {
            "data": [{"id": 1}, {"id": 2}],
            "router_dep": router_dep,
            "app_dep": global_dep,
        }


payment_router = Router(
    "/payments",
    route_handlers=[PaymentController, get_audit_trail],
    dependencies={"router_dep": Provide(provide_router_dependency)},
    tags=["payments"],
)

route_handlers = [
    hello,
    ProductController,
    SupplierController,
    PurchaseOrderController,
    SupplierInvoiceController,
    DummyController,
    payment_router,
]


app = Litestar(
    route_handlers=route_handlers,
    plugins=[sqla_plugin],
    dependencies={"global_dep": Provide(provide_global_dependency)},
)
