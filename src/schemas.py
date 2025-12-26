from dataclasses import dataclass, field
from decimal import Decimal
from enum import Enum
from datetime import datetime

class CategoryEnum(Enum):
    electronics = "Electronics"
    medical = "Medical"
    food = "Food"

class StatusEnum(Enum):
    DRAFT = "Draft"
    PUBLIC = "Public"

@dataclass
class ProductReadSchema:
    id: int
    name: str
    description: str
    category: CategoryEnum
    unit_price: Decimal = Decimal("0")
    cost_price: Decimal = Decimal("0")
    status : StatusEnum = StatusEnum.DRAFT
    size: str = None
    color: str = None
    weight: int =0
    weight_unit: str ="kg"
    width: Decimal = None
    height: Decimal = None
    dimensions_unit: str = "cm"
    stock: int = 0
    country_of_origin: str = None
    product_metadata: dict = field(default_factory={})
    updated_at: datetime = None
    created_at: datetime = None


@dataclass
class ProductWriteSchema:
    name: str
    description: str
    category: CategoryEnum
    unit_price: Decimal = Decimal("0")
    cost_price: Decimal = Decimal("0")
    status : StatusEnum = StatusEnum.DRAFT
    size: str = None
    color: str = None
    weight: int = 0
    weight_unit: str = "kg"
    width: Decimal = None
    height: Decimal = None
    dimensions_unit: str = "cm"
    stock: int = 0
    country_of_origin: str = None
    product_metadata: dict = field(default_factory={})



