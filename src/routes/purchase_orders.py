from dataclasses import asdict

from advanced_alchemy.exceptions import NotFoundError
from litestar import Controller, delete, get, post, put
from litestar.di import Provide
from litestar.exceptions import ClientException, NotFoundException
from sqlalchemy.ext.asyncio import AsyncSession

from src.db.dependencies import (
    provide_product_repo,
    provide_purchase_order_repo,
    provide_supplier_repo,
)
from src.db.models import PurchaseOrderItemModel, PurchaseOrderModel
from src.db.repositories import (
    ProductRepository,
    PurchaseOrderRepository,
    SupplierRepository,
)
from src.schemas.purchase_orders import (
    PurchaseOrderReadSchema,
    PurchaseOrderWriteSchema,
)


class PurchaseOrderController(Controller):
    path = "/purchase-orders"
    tags = ["Purchase Order Endpoints"]
    dependencies = {
        "po_repo": Provide(provide_purchase_order_repo),
        "supplier_repo": Provide(provide_supplier_repo),
        "product_repo": Provide(provide_product_repo),
    }

    @get("/")
    async def list_purchase_orders(
        self, po_repo: PurchaseOrderRepository
    ) -> list[PurchaseOrderReadSchema]:
        pos = await po_repo.list()
        return [PurchaseOrderReadSchema(**po.to_dict()) for po in pos]

    @get("/{po_id:int}")
    async def get_purchase_order(
        self, po_id: int, po_repo: PurchaseOrderRepository
    ) -> PurchaseOrderReadSchema:
        try:
            po = await po_repo.get(item_id=po_id)
            return PurchaseOrderReadSchema(**po.to_dict())
        except NotFoundError:
            raise NotFoundException(detail="Purchase Order not found")

    @post("/")
    async def create_purchase_order(
        self,
        data: PurchaseOrderWriteSchema,
        po_repo: PurchaseOrderRepository,
        supplier_repo: SupplierRepository,
        product_repo: ProductRepository,
        db_session: AsyncSession,
    ) -> PurchaseOrderReadSchema:
        # 1. Validate Supplier
        supplier = await supplier_repo.get_one_or_none(id=data.supplier_id)
        if not supplier:
            raise NotFoundException(
                detail=f"Supplier with ID {data.supplier_id} not found"
            )

        # 2. Validate Products & Prepare Items
        items_data = []
        data_dict = asdict(data)
        items = data_dict.pop("items", [])

        for item in items:
            product = await product_repo.get_one_or_none(id=item["product_id"])
            if not product:
                raise NotFoundException(
                    detail=f"Product with ID {item['product_id']} not found"
                )
            items_data.append(PurchaseOrderItemModel(**item))

        # 3. Create PO
        po_model = PurchaseOrderModel(**data_dict)
        po_model.items = items_data

        new_po = await po_repo.add(po_model)
        await db_session.commit()

        return PurchaseOrderReadSchema(**new_po.to_dict())

    @put("/{po_id:int}")
    async def update_purchase_order(
        self,
        po_id: int,
        data: PurchaseOrderWriteSchema,
        po_repo: PurchaseOrderRepository,
        db_session: AsyncSession,
    ) -> PurchaseOrderReadSchema:
        try:
            data_dict = asdict(data)
            _ = data_dict.pop(
                "items", []
            )  # Handle item updates separately or ignore for now?

            data_dict["id"] = po_id
            updated_po = await po_repo.update(PurchaseOrderModel(**data_dict))
            updated_po.items = data.items
            await db_session.commit()
            return PurchaseOrderReadSchema(**updated_po.to_dict())
        except NotFoundError:
            raise NotFoundException(detail="Purchase Order Not Found")

    @delete("/{po_id:int}")
    async def delete_purchase_order(
        self,
        po_id: int,
        po_repo: PurchaseOrderRepository,
        db_session: AsyncSession,
    ) -> None:
        try:
            await po_repo.delete(item_id=po_id)
            await db_session.commit()
        except NotFoundError:
            raise NotFoundException(detail="Purchase Order Not Found")
