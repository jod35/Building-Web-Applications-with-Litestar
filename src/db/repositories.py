from litestar.plugins.sqlalchemy import repository

from src.db.models import ProductModel


class ProductRepository(repository.SQLAlchemyAsyncRepository[ProductModel]):
    model_type = ProductModel
