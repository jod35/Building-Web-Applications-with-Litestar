from dataclasses import asdict

from advanced_alchemy.exceptions import NotFoundError
from litestar import Controller, delete, get, post, put
from litestar.di import Provide
from litestar.exceptions import NotFoundException
from sqlalchemy.ext.asyncio import AsyncSession

from src.db.dependencies import provide_product_repo
from src.db.models import ProductModel
from src.db.repositories import ProductRepository
from src.schemas import ProductReadSchema, ProductWriteSchema


class ProductController(Controller):
    path = "/products"
    dependencies = {"product_repo": Provide(provide_product_repo)}

    @get("/")
    async def list_products(
        self, product_repo: ProductRepository
    ) -> list[ProductReadSchema]:
        products = await product_repo.list()

        return [ProductReadSchema(**product.to_dict()) for product in products]

    @get("/{product_id:int}")
    async def get_product_by_id(
        self, product_id: int, product_repo: ProductRepository
    ) -> ProductReadSchema:
        try:
            product = await product_repo.get(item_id=product_id)
            return ProductReadSchema(**product.to_dict())
        except NotFoundError:
            raise NotFoundException(detail="Product not found")

    @post("/")
    async def create_product(
        self,
        data: ProductWriteSchema,
        db_session: AsyncSession,
        product_repo: ProductRepository,
    ) -> ProductReadSchema:
        # convert schema data to dict
        data_dict = asdict(data)

        new_product = await product_repo.add(ProductModel(**data_dict))

        await db_session.commit()

        return ProductReadSchema(**new_product.to_dict())

    @put("/{product_id:int}")
    async def update_product(
        self,
        product_id: int,
        data: ProductWriteSchema,
        product_repo: ProductRepository,
        db_session: AsyncSession,
    ) -> ProductReadSchema:
        try:
            data_dict = asdict(data)

            data_dict["id"] = product_id
            updated_product = await product_repo.update(ProductModel(**data_dict))
            await db_session.commit()
            return ProductReadSchema(**updated_product.to_dict())
        except NotFoundError:
            raise NotFoundException(detail="Product Not Found")

    @delete("/{product_id:int}")
    async def delete_product(
        self,
        product_id: int,
        product_repo: ProductRepository,
        db_session: AsyncSession,
    ) -> None:
        try:
            await product_repo.delete(item_id=product_id)
            await db_session.commit()
        except NotFoundError:
            raise NotFoundException(detail="Product Not Found")
