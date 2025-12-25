from litestar import Controller, get, post, put ,delete
from src.schemas import ProductRead, ProductWrite

class ProductController(Controller):
    path = "/products"

    @get('/')
    async def list_products(self) -> list[ProductRead]:
        ...

    @get('/{product_id:int}')
    async def get_product_by_id(self,product_id:int) -> ProductRead:
        ...

    @post('/')
    async def create_product(self,data:ProductWrite) -> ProductRead:
        ...

    @put('/{product_id:int}')
    async def update_product(self,product_id:int , data: ProductWrite) -> ProductRead:
        ...

    @delete('/{product_id:int}')
    async def delete_product(self,product_id:int) -> None:
        ...