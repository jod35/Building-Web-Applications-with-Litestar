from sqlalchemy.ext.asyncio import AsyncSession

from src.db.repositories import ProductRepository, SupplierRepository, PurchaseOrderRepository, SupplierInvoiceRepository


async def provide_product_repo(db_session: AsyncSession) -> ProductRepository:
    return ProductRepository(session=db_session)


async def provide_supplier_repo(db_session: AsyncSession) -> SupplierRepository:
    return SupplierRepository(session=db_session)


async def provide_purchase_order_repo(db_session: AsyncSession) -> PurchaseOrderRepository:
    return PurchaseOrderRepository(session=db_session)


async def provide_supplier_invoice_repo(db_session: AsyncSession) -> SupplierInvoiceRepository:
    return SupplierInvoiceRepository(session=db_session)
