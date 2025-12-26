from litestar import Controller, get, post, put ,delete
from src.schemas import ProductReadSchema, ProductWriteSchema

class ProductController(Controller):
    path = "/products"

    @get('/')
    async def list_products(self) -> list[ProductReadSchema]:
        ...

    @get('/{product_id:int}')
    async def get_product_by_id(self,product_id:int) -> ProductReadSchema:
        ...

    @post('/')
    async def create_product(self,data:ProductWriteSchema) -> ProductReadSchema:
        ...

    @put('/{product_id:int}')
    async def update_product(self,product_id:int , data: ProductWriteSchema) -> ProductReadSchema:
        ...

    @delete('/{product_id:int}')
    async def delete_product(self,product_id:int) -> None:
        ...