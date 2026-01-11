from litestar.plugins.sqlalchemy import repository

from src.db.models import ProductModel, SupplierModel


class ProductRepository(repository.SQLAlchemyAsyncRepository[ProductModel]):
    model_type = ProductModel


class SupplierRepository(repository.SQLAlchemyAsyncRepository[SupplierModel]):
    model_type = SupplierModel
