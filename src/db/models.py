from decimal import Decimal
from typing import Optional

from litestar.plugins.sqlalchemy import BigIntAuditBase
from sqlalchemy.dialects.mysql import DECIMAL, ENUM, INTEGER, JSON, TEXT, VARCHAR
from sqlalchemy.orm import Mapped, mapped_column

from src.schemas import CategoryEnum, StatusEnum


class ProductModel(BigIntAuditBase):
    __tablename__ = "products"

    name: Mapped[str] = mapped_column(VARCHAR(255), nullable=False)
    description: Mapped[str] = mapped_column(TEXT, nullable=False)
    category: Mapped[CategoryEnum] = mapped_column(ENUM(CategoryEnum), nullable=False)
    unit_price: Mapped[Decimal] = mapped_column(DECIMAL(10, 2), default=Decimal("0"))
    cost_price: Mapped[Decimal] = mapped_column(DECIMAL(10, 2), default=Decimal("0"))
    status: Mapped[StatusEnum] = mapped_column(
        ENUM(StatusEnum), default=StatusEnum.DRAFT
    )
    size: Mapped[Optional[str]] = mapped_column(VARCHAR(50), nullable=True)
    color: Mapped[Optional[str]] = mapped_column(VARCHAR(50), nullable=True)
    weight: Mapped[int] = mapped_column(INTEGER, default=0)
    weight_unit: Mapped[str] = mapped_column(VARCHAR(10), default="kg")
    width: Mapped[Optional[Decimal]] = mapped_column(DECIMAL(10, 2), nullable=True)
    height: Mapped[Optional[Decimal]] = mapped_column(DECIMAL(10, 2), nullable=True)
    dimensions_unit: Mapped[str] = mapped_column(VARCHAR(10), default="cm")
    stock: Mapped[int] = mapped_column(INTEGER, default=0)
    country_of_origin: Mapped[Optional[str]] = mapped_column(
        VARCHAR(100), nullable=True
    )
    product_metadata: Mapped[dict] = mapped_column(JSON, default=dict)

    def __repr__(self):
        return f"<ProductModel {self.name}>"
