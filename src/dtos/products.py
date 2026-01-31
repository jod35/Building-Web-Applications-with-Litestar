from litestar.dto import DataclassDTO
from litestar.dto.config import DTOConfig


from src.schemas.products import ProductReadSchema


class ProductDTO(DataclassDTO[ProductReadSchema]): 
    config = DTOConfig(
        exclude={'id','created_at','updated_at'}
    )

class ProductReturnDTO(DataclassDTO[ProductReadSchema]): 
    config = DTOConfig(
        # exclude={'product_metadata'}
        rename_fields={'product_metadata':'product_metadata'},
        rename_strategy="camel"
    )

