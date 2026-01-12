from litestar.plugins.sqlalchemy import BigIntAuditBase
from sqlalchemy import ForeignKey, func
from sqlalchemy.dialects.mysql import DATETIME, DECIMAL, TEXT, VARCHAR, INTEGER
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import List, Optional
from datetime import datetime
from decimal import Decimal
from enum import Enum

from . import *


class PurchaseOrderStatus(str, Enum):
    DRAFT = "DRAFT"
    SENT = "SENT"
    APPROVED = "APPROVED"
    PARTIALLY_RECEIVED = "PARTIALLY_RECEIVED"
    COMPLETED = "COMPLETED"
    CANCELLED = "CANCELLED"


class PurchaseOrderModel(BigIntAuditBase):
    """
    Purchase Order sent to supplier
    """

    __tablename__ = "purchase_orders"

    po_number: Mapped[str] = mapped_column(
        VARCHAR(40), unique=True, index=True, nullable=False
    )
    supplier_id: Mapped[int] = mapped_column(
        ForeignKey("suppliers.id", ondelete="RESTRICT"), nullable=False
    )
    order_date: Mapped[datetime] = mapped_column(
        DATETIME(timezone=True), server_default=func.now(), nullable=False
    )
    expected_delivery_date: Mapped[Optional[datetime]] = mapped_column(
        DATETIME(timezone=True)
    )

    status: Mapped[PurchaseOrderStatus] = mapped_column(
        VARCHAR(30), default=PurchaseOrderStatus.DRAFT, nullable=False
    )

    subtotal: Mapped[Decimal] = mapped_column(DECIMAL(14, 2), default=Decimal("0.00"))
    discount_amount: Mapped[Decimal] = mapped_column(
        DECIMAL(14, 2), default=Decimal("0.00")
    )
    total_amount: Mapped[Decimal] = mapped_column(DECIMAL(14, 2), nullable=False)

    paid_amount: Mapped[Decimal] = mapped_column(
        DECIMAL(14, 2), default=Decimal("0.00")
    )

    notes: Mapped[Optional[str]] = mapped_column(TEXT)

    supplier: Mapped["SupplierModel"] = relationship(back_populates="purchase_orders")
    items: Mapped[List["PurchaseOrderItemModel"]] = relationship(
        back_populates="purchase_order", lazy="selectin"
    )

    def __repr__(self) -> str:
        return f"<PurchaseOrder {self.po_number} ({self.status})>"


class PurchaseOrderItemModel(BigIntAuditBase):
    """
    Line item in a Purchase Order
    """

    __tablename__ = "purchase_order_items"

    purchase_order_id: Mapped[int] = mapped_column(
        ForeignKey("purchase_orders.id", ondelete="CASCADE"), nullable=False
    )
    product_id: Mapped[int] = mapped_column(
        ForeignKey("products.id", ondelete="RESTRICT"), nullable=False
    )

    quantity_ordered: Mapped[int] = mapped_column(INTEGER, nullable=False)
    quantity_received: Mapped[int] = mapped_column(INTEGER, default=0)

    unit_price: Mapped[Decimal] = mapped_column(DECIMAL(12, 2), nullable=False)
    discount_amount: Mapped[Decimal] = mapped_column(
        DECIMAL(12, 2), default=Decimal("0.00")
    )
    subtotal: Mapped[Decimal] = mapped_column(DECIMAL(14, 2), nullable=False)

    notes: Mapped[Optional[str]] = mapped_column(TEXT)

    # relationships
    purchase_order: Mapped["PurchaseOrderModel"] = relationship(back_populates="items")
    product: Mapped["ProductModel"] = relationship(
        back_populates="purchase_order_items"
    )

    def __repr__(self) -> str:
        return f"<POItem PO:{self.purchase_order_id} Prod:{self.product_id}>"
