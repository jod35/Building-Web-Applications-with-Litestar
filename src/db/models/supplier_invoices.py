from litestar.plugins.sqlalchemy import BigIntAuditBase
from sqlalchemy import ForeignKey, func, UniqueConstraint
from sqlalchemy.dialects.mysql import DATETIME, DECIMAL, TEXT, VARCHAR, ENUM, INTEGER
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import List, Optional
from datetime import datetime
from decimal import Decimal
from enum import Enum

from .suppliers import SupplierModel
from .products import ProductModel
from .purchase_orders import PurchaseOrderModel, PurchaseOrderItemModel

class InvoiceStatusEnum(Enum):
    """Status of a supplier invoice"""
    DRAFT = "DRAFT"
    UNPAID = "UNPAID"
    PARTIALLY_PAID = "PARTIALLY_PAID"
    PAID = "PAID"
    CANCELLED = "CANCELLED"
    VOID = "VOID"


class PaymentStatusEnum(Enum):
    """Overall payment status"""
    PENDING = "PENDING"
    PARTIAL = "PARTIAL"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"



class SupplierInvoiceModel(BigIntAuditBase):
    """
    Supplier Invoice / Bill (Purchase Invoice)
    """
    __tablename__ = "supplier_invoices"

    invoice_number: Mapped[str] = mapped_column(VARCHAR(60), index=True, nullable=False)
    supplier_id: Mapped[int] = mapped_column(
        ForeignKey("suppliers.id", ondelete="RESTRICT"), nullable=False
    )
    purchase_order_id: Mapped[Optional[int]] = mapped_column(
        ForeignKey("purchase_orders.id", ondelete="SET NULL"), nullable=True
    )
    invoice_date: Mapped[datetime] = mapped_column(DATETIME(timezone=True), nullable=False)
    due_date: Mapped[Optional[datetime]] = mapped_column(DATETIME(timezone=True))

    status: Mapped[InvoiceStatusEnum] = mapped_column(
        ENUM(InvoiceStatusEnum), default=InvoiceStatusEnum.UNPAID
    )
    payment_status: Mapped[PaymentStatusEnum] = mapped_column(
        ENUM(PaymentStatusEnum), default=PaymentStatusEnum.PENDING
    )
    subtotal: Mapped[Decimal] = mapped_column(DECIMAL(14, 2), default=Decimal("0.00"))
    other_charges: Mapped[Decimal] = mapped_column(DECIMAL(14, 2), default=Decimal("0.00"))
    discount_amount: Mapped[Decimal] = mapped_column(DECIMAL(14, 2), default=Decimal("0.00"))
    total_amount: Mapped[Decimal] = mapped_column(DECIMAL(14, 2), nullable=False)

    amount_paid: Mapped[Decimal] = mapped_column(DECIMAL(14, 2), default=Decimal("0.00"))
    balance_due: Mapped[Decimal] = mapped_column(DECIMAL(14, 2), nullable=False)

    currency: Mapped[str] = mapped_column(VARCHAR(3), default="USD")
    notes: Mapped[Optional[str]] = mapped_column(TEXT)

    supplier: Mapped[SupplierModel] = relationship()
    purchase_order: Mapped[Optional["PurchaseOrderModel"]] = relationship()
    items: Mapped[List["SupplierInvoiceItemModel"]] = relationship(
        back_populates="invoice", cascade="all, delete-orphan"
    )

    __table_args__ = (
        UniqueConstraint("supplier_id", "invoice_number", name="uq_supplier_invoice"),
    )

    def __repr__(self) -> str:
        return f"<SupplierInvoice {self.invoice_number} ({self.status})>"


class SupplierInvoiceItemModel(BigIntAuditBase):
    """
    Line item on supplier invoice
    """
    __tablename__ = "supplier_invoice_items"

    invoice_id: Mapped[int] = mapped_column(
        ForeignKey("supplier_invoices.id", ondelete="CASCADE"), nullable=False
    )
    product_id: Mapped[int] = mapped_column(
        ForeignKey("products.id", ondelete="RESTRICT"), nullable=False
    )
    purchase_order_item_id: Mapped[Optional[int]] = mapped_column(
        ForeignKey("purchase_order_items.id", ondelete="SET NULL"), nullable=True
    )

    quantity: Mapped[int] = mapped_column(INTEGER, nullable=False)
    unit_price: Mapped[Decimal] = mapped_column(DECIMAL(12, 2), nullable=False)
    discount_amount: Mapped[Decimal] = mapped_column(DECIMAL(12, 2), default=Decimal("0.00"))
    subtotal: Mapped[Decimal] = mapped_column(DECIMAL(14, 2), nullable=False)

    received_quantity: Mapped[Optional[int]] = mapped_column(INTEGER)

    notes: Mapped[Optional[str]] = mapped_column(TEXT)

    invoice: Mapped[SupplierInvoiceModel] = relationship(back_populates="items")
    product: Mapped[ProductModel] = relationship(back_populates="supplier_invoice_items")
    purchase_order_item: Mapped[Optional[PurchaseOrderItemModel]] = relationship()

    def __repr__(self) -> str:
        return f"<InvItem Inv:{self.invoice_id} Prod:{self.product_id}>"


