from dataclasses import asdict

from advanced_alchemy.exceptions import NotFoundError
from litestar import Controller, delete, get, post, put
from litestar.di import Provide
from litestar.exceptions import NotFoundException
from sqlalchemy.ext.asyncio import AsyncSession

from src.db.dependencies import (
    provide_purchase_order_repo,
    provide_supplier_invoice_repo,
    provide_supplier_repo,
    provide_product_repo,
)
from src.db.models import SupplierInvoiceModel, SupplierInvoiceItemModel
from src.db.repositories import (
    PurchaseOrderRepository,
    SupplierInvoiceRepository,
    SupplierRepository,
    ProductRepository,
)
from src.schemas.supplier_invoices import (
    SupplierInvoiceReadSchema,
    SupplierInvoiceWriteSchema,
)


class SupplierInvoiceController(Controller):
    path = "/supplier-invoices"
    dependencies = {
        "invoice_repo": Provide(provide_supplier_invoice_repo),
        "supplier_repo": Provide(provide_supplier_repo),
        "po_repo": Provide(provide_purchase_order_repo),
        "product_repo": Provide(provide_product_repo),
    }

    @get("/")
    async def list_invoices(
        self, invoice_repo: SupplierInvoiceRepository
    ) -> list[SupplierInvoiceReadSchema]:
        invoices = await invoice_repo.list()
        return [SupplierInvoiceReadSchema(**inv.to_dict()) for inv in invoices]

    @get("/{invoice_id:int}")
    async def get_invoice(
        self, invoice_id: int, invoice_repo: SupplierInvoiceRepository
    ) -> SupplierInvoiceReadSchema:
        try:
            inv = await invoice_repo.get(item_id=invoice_id)
            return SupplierInvoiceReadSchema(**inv.to_dict())
        except NotFoundError:
            raise NotFoundException(detail="Supplier Invoice not found")

    @post("/")
    async def create_invoice(
        self,
        data: SupplierInvoiceWriteSchema,
        invoice_repo: SupplierInvoiceRepository,
        supplier_repo: SupplierRepository,
        po_repo: PurchaseOrderRepository,
        product_repo: ProductRepository,
        db_session: AsyncSession,
    ) -> SupplierInvoiceReadSchema:
        # 1. Validate Supplier
        supplier = await supplier_repo.get_one_or_none(id=data.supplier_id)
        if not supplier:
            raise NotFoundException(detail=f"Supplier with ID {data.supplier_id} not found")

        # 2. Validate Purchase Order (if provided)
        if data.purchase_order_id:
            po = await po_repo.get_one_or_none(id=data.purchase_order_id)
            if not po:
                raise NotFoundException(detail=f"Purchase Order with ID {data.purchase_order_id} not found")

        # 3. Validate Products & Prepare Items
        items_data = []
        data_dict = asdict(data)
        items = data_dict.pop("items", [])

        for item in items:
            product = await product_repo.get_one_or_none(id=item["product_id"])
            if not product:
                raise NotFoundException(detail=f"Product with ID {item['product_id']} not found")
            
            # TODO: Validate purchase_order_item_id if provided?
            # For now, simplistic validation.
            
            items_data.append(SupplierInvoiceItemModel(**item))

        # 4. Create Invoice
        invoice_model = SupplierInvoiceModel(**data_dict)
        invoice_model.items = items_data

        new_invoice = await invoice_repo.add(invoice_model)
        await db_session.commit()

        return SupplierInvoiceReadSchema(**new_invoice.to_dict())

    @put("/{invoice_id:int}")
    async def update_invoice(
        self,
        invoice_id: int,
        data: SupplierInvoiceWriteSchema,
        invoice_repo: SupplierInvoiceRepository,
        db_session: AsyncSession,
    ) -> SupplierInvoiceReadSchema:
        try:
            data_dict = asdict(data)
            items = data_dict.pop("items", []) # Handle items separately

            data_dict["id"] = invoice_id
            updated_invoice = await invoice_repo.update(SupplierInvoiceModel(**data_dict))
            
            # Simple item update: replace all? OR just let user handle items via separate endpoint?
            # Matching user's PO pattern:
            updated_invoice.items = [SupplierInvoiceItemModel(**item) for item in items]
            
            await db_session.commit()
            return SupplierInvoiceReadSchema(**updated_invoice.to_dict())
        except NotFoundError:
            raise NotFoundException(detail="Supplier Invoice Not Found")

    @delete("/{invoice_id:int}")
    async def delete_invoice(
        self,
        invoice_id: int,
        invoice_repo: SupplierInvoiceRepository,
        db_session: AsyncSession,
    ) -> None:
        try:
            await invoice_repo.delete(item_id=invoice_id)
            await db_session.commit()
        except NotFoundError:
            raise NotFoundException(detail="Supplier Invoice Not Found")