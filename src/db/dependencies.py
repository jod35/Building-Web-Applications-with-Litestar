from sqlalchemy.ext.asyncio import AsyncSession

from src.db.repositories import ProductRepository, SupplierRepository


async def provide_product_repo(db_session: AsyncSession) -> ProductRepository:
    return ProductRepository(session=db_session)


async def provide_supplier_repo(db_session: AsyncSession) -> SupplierRepository:
    return SupplierRepository(session=db_session)
