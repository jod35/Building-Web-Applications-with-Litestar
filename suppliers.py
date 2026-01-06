from datetime import datetime
from decimal import Decimal
import enum
from typing import List, Optional

from litestar.plugins.sqlalchemy import BigIntAuditBase
from sqlalchemy import ForeignKey, UniqueConstraint, func
from sqlalchemy.dialects.mysql import (
    DECIMAL, ENUM, INTEGER, VARCHAR, TEXT, DATETIME, JSON
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

# Assuming these are defined in src.schemas
from src.schemas import CategoryEnum, StatusEnum


# ────────────────────────────────────────────────────────────────
#                        Shared Enums
# ────────────────────────────────────────────────────────────────

class InvoiceStatusEnum(str, enum.Enum):
    """Status of a supplier invoice"""
    DRAFT = "DRAFT"
    UNPAID = "UNPAID"
    PARTIALLY_PAID = "PARTIALLY_PAID"
    PAID = "PAID"
    CANCELLED = "CANCELLED"
    VOID = "VOID"


class PaymentStatusEnum(str, enum.Enum):
    """Overall payment status"""
    PENDING = "PENDING"
    PARTIAL = "PARTIAL"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"


# ────────────────────────────────────────────────────────────────
#                           CORE MODELS
# ────────────────────────────────────────────────────────────────

class ProductModel(BigIntAuditBase):
    """
    Core product entity for inventory/POS system
    """
    __tablename__ = "products"

    name: Mapped[str] = mapped_column(VARCHAR(255), nullable=False, doc="Product display name")
    description: Mapped[str] = mapped_column(TEXT, nullable=False)
    category: Mapped[CategoryEnum] = mapped_column(ENUM(CategoryEnum), nullable=False)
    
    unit_price: Mapped[Decimal] = mapped_column(DECIMAL(12, 2), default=Decimal("0.00"), doc="Selling price")
    cost_price: Mapped[Decimal] = mapped_column(DECIMAL(12, 2), default=Decimal("0.00"), doc="Purchase/cost price")
    
    status: Mapped[StatusEnum] = mapped_column(
        ENUM(StatusEnum), default=StatusEnum.DRAFT, nullable=False
    )
    
    size: Mapped[Optional[str]] = mapped_column(VARCHAR(50), nullable=True)
    color: Mapped[Optional[str]] = mapped_column(VARCHAR(50), nullable=True)
    
    weight: Mapped[int] = mapped_column(INTEGER, default=0)
    weight_unit: Mapped[str] = mapped_column(VARCHAR(10), default="kg")
    
    width: Mapped[Optional[Decimal]] = mapped_column(DECIMAL(10, 2), nullable=True)
    height: Mapped[Optional[Decimal]] = mapped_column(DECIMAL(10, 2), nullable=True)
    dimensions_unit: Mapped[str] = mapped_column(VARCHAR(10), default="cm")
    
    stock: Mapped[int] = mapped_column(INTEGER, default=0, doc="Current stock quantity")
    low_stock_threshold: Mapped[int] = mapped_column(INTEGER, default=10)
    
    supplier_id: Mapped[Optional[int]] = mapped_column(
        ForeignKey("suppliers.id", ondelete="SET NULL"), nullable=True
    )
    country_of_origin: Mapped[Optional[str]] = mapped_column(VARCHAR(100), nullable=True)
    
    product_metadata: Mapped[dict] = mapped_column(JSON, default=dict, doc="Flexible JSON metadata")

    # Relationships (add these when you have variants, orders, etc.)
    # variants: Mapped[List["ProductVariantModel"]] = relationship(back_populates="product")
    purchase_order_items: Mapped[List["PurchaseOrderItemModel"]] = relationship(back_populates="product")
    supplier_invoice_items: Mapped[List["SupplierInvoiceItemModel"]] = relationship(back_populates="product")

    def __repr__(self) -> str:
        return f"<Product {self.name} (#{self.id})>"


class SupplierModel(BigIntAuditBase):
    """
    Supplier / Vendor master data
    """
    __tablename__ = "suppliers"

    name: Mapped[str] = mapped_column(VARCHAR(150), nullable=False, index=True)
    company_name: Mapped[Optional[str]] = mapped_column(VARCHAR(200))
    contact_person: Mapped[Optional[str]] = mapped_column(VARCHAR(100))
    email: Mapped[Optional[str]] = mapped_column(VARCHAR(255))
    phone: Mapped[Optional[str]] = mapped_column(VARCHAR(30))
    mobile: Mapped[Optional[str]] = mapped_column(VARCHAR(30))
    website: Mapped[Optional[str]] = mapped_column(VARCHAR(255))

    address_line1: Mapped[Optional[str]] = mapped_column(VARCHAR(255))
    city: Mapped[Optional[str]] = mapped_column(VARCHAR(100))
    country: Mapped[Optional[str]] = mapped_column(VARCHAR(100))

    currency: Mapped[str] = mapped_column(VARCHAR(3), default="USD")

    is_active: Mapped[bool] = mapped_column(default=True)
    notes: Mapped[Optional[str]] = mapped_column(TEXT)

    # Relationships
    purchase_orders: Mapped[List["PurchaseOrderModel"]] = relationship(
        back_populates="supplier", cascade="all, delete-orphan"
    )
    products: Mapped[List["ProductModel"]] = relationship(back_populates="supplier")

    def __repr__(self) -> str:
        return f"<Supplier {self.name} ({self.company_name or 'N/A'})>"


class PurchaseOrderModel(BigIntAuditBase):
    """
    Purchase Order sent to supplier
    """
    __tablename__ = "purchase_orders"

    po_number: Mapped[str] = mapped_column(VARCHAR(40), unique=True, index=True, nullable=False)
    supplier_id: Mapped[int] = mapped_column(
        ForeignKey("suppliers.id", ondelete="RESTRICT"), nullable=False
    )
    order_date: Mapped[datetime] = mapped_column(
        DATETIME(timezone=True), server_default=func.now(), nullable=False
    )
    expected_delivery_date: Mapped[Optional[datetime]] = mapped_column(DATETIME(timezone=True))

    status: Mapped[str] = mapped_column(
        VARCHAR(30), default="DRAFT", nullable=False,
        doc="DRAFT, SENT, APPROVED, PARTIALLY_RECEIVED, COMPLETED, CANCELLED"
    )

    subtotal: Mapped[Decimal] = mapped_column(DECIMAL(14, 2), default=Decimal("0.00"))
    discount_amount: Mapped[Decimal] = mapped_column(DECIMAL(14, 2), default=Decimal("0.00"))
    total_amount: Mapped[Decimal] = mapped_column(DECIMAL(14, 2), nullable=False)

    paid_amount: Mapped[Decimal] = mapped_column(DECIMAL(14, 2), default=Decimal("0.00"))

    notes: Mapped[Optional[str]] = mapped_column(TEXT)

    supplier: Mapped["SupplierModel"] = relationship(back_populates="purchase_orders")
    items: Mapped[List["PurchaseOrderItemModel"]] = relationship(
        back_populates="purchase_order", cascade="all, delete-orphan"
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
    discount_amount: Mapped[Decimal] = mapped_column(DECIMAL(12, 2), default=Decimal("0.00"))
    subtotal: Mapped[Decimal] = mapped_column(DECIMAL(14, 2), nullable=False)

    notes: Mapped[Optional[str]] = mapped_column(TEXT)

    purchase_order: Mapped["PurchaseOrderModel"] = relationship(back_populates="items")
    product: Mapped["ProductModel"] = relationship(back_populates="purchase_order_items")

    def __repr__(self) -> str:
        return f"<POItem PO:{self.purchase_order_id} Prod:{self.product_id}>"


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

    supplier: Mapped["SupplierModel"] = relationship()
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

    invoice: Mapped["SupplierInvoiceModel"] = relationship(back_populates="items")
    product: Mapped["ProductModel"] = relationship(back_populates="supplier_invoice_items")
    purchase_order_item: Mapped[Optional["PurchaseOrderItemModel"]] = relationship()

    def __repr__(self) -> str:
        return f"<InvItem Inv:{self.invoice_id} Prod:{self.product_id}>"


