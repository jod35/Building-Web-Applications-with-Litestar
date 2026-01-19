from dataclasses import asdict

from advanced_alchemy.exceptions import NotFoundError
from litestar import Controller, delete, get, post, put
from litestar.di import Provide
from litestar.exceptions import NotFoundException
from sqlalchemy.ext.asyncio import AsyncSession

from src.db.dependencies import provide_supplier_repo
from src.db.models import SupplierModel
from src.db.repositories import SupplierRepository
from src.schemas.suppliers import SupplierReadSchema, SupplierWriteSchema


class SupplierController(Controller):
    path = "/suppliers"
    dependencies = {"supplier_repo": Provide(provide_supplier_repo)}

    @get("/")
    async def list_suppliers(
        self, supplier_repo: SupplierRepository
    ) -> list[SupplierReadSchema]:
        suppliers = await supplier_repo.list()
        return [SupplierReadSchema(**supplier.to_dict()) for supplier in suppliers]

    @get("/{supplier_id:int}")
    async def get_supplier_by_id(
        self, supplier_id: int, supplier_repo: SupplierRepository
    ) -> SupplierReadSchema:
        try:
            supplier = await supplier_repo.get(item_id=supplier_id)
            return SupplierReadSchema(**supplier.to_dict())
        except NotFoundError:
            raise NotFoundException(detail="Supplier not found")

    @post("/")
    async def create_supplier(
        self,
        data: SupplierWriteSchema,
        db_session: AsyncSession,
        supplier_repo: SupplierRepository,
    ) -> SupplierReadSchema:
        data_dict = asdict(data)
        new_supplier = await supplier_repo.add(SupplierModel(**data_dict))
        await db_session.commit()
        return SupplierReadSchema(**new_supplier.to_dict())

    @put("/{supplier_id:int}")
    async def update_supplier(
        self,
        supplier_id: int,
        data: SupplierWriteSchema,
        supplier_repo: SupplierRepository,
        db_session: AsyncSession,
    ) -> SupplierReadSchema:
        try:
            data_dict = asdict(data)
            data_dict["id"] = supplier_id
            updated_supplier = await supplier_repo.update(SupplierModel(**data_dict))
            await db_session.commit()
            return SupplierReadSchema(**updated_supplier.to_dict())
        except NotFoundError:
            raise NotFoundException(detail="Supplier Not Found")

    @delete("/{supplier_id:int}")
    async def delete_supplier(
        self,
        supplier_id: int,
        supplier_repo: SupplierRepository,
        db_session: AsyncSession,
    ) -> None:
        try:
            await supplier_repo.delete(item_id=supplier_id)
            await db_session.commit()
        except NotFoundError:
            raise NotFoundException(detail="Supplier Not Found")
