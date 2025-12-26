from sqlalchemy.ext.asyncio import AsyncSession

from src.db.repositories import ProductRepository


async def provide_product_repo(db_session: AsyncSession) -> ProductRepository:
    return ProductRepository(session=db_session)
