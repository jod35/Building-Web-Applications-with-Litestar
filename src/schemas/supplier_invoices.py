from dataclasses import dataclass, field
from datetime import datetime
from decimal import Decimal
from typing import Optional, List

from src.db.models.supplier_invoices import InvoiceStatusEnum, PaymentStatusEnum


@dataclass
class SupplierInvoiceItemReadSchema:
    id: int
    invoice_id: int
    product_id: int
    purchase_order_item_id: Optional[int]
    quantity: int
    unit_price: Decimal
    discount_amount: Decimal
    subtotal: Decimal
    received_quantity: Optional[int]
    notes: Optional[str]
    created_at: datetime
    updated_at: datetime


@dataclass
class SupplierInvoiceItemWriteSchema:
    product_id: int
    quantity: int
    unit_price: Decimal
    subtotal: Decimal
    purchase_order_item_id: Optional[int] = None
    discount_amount: Decimal = Decimal("0.00")
    received_quantity: int = 0
    notes: Optional[str] = None


@dataclass
class SupplierInvoiceReadSchema:
    id: int
    invoice_number: str
    supplier_id: int
    purchase_order_id: Optional[int]
    invoice_date: datetime
    due_date: Optional[datetime]
    status: InvoiceStatusEnum
    payment_status: PaymentStatusEnum
    subtotal: Decimal
    other_charges: Decimal
    discount_amount: Decimal
    total_amount: Decimal
    amount_paid: Decimal
    balance_due: Decimal
    currency: str
    notes: Optional[str]
    # items: List[SupplierInvoiceItemReadSchema] # Optional: include items?
    created_at: datetime
    updated_at: datetime


@dataclass
class SupplierInvoiceWriteSchema:
    invoice_number: str
    supplier_id: int
    total_amount: Decimal
    balance_due: Decimal
    invoice_date: datetime = field(default_factory=datetime.now)
    items: List[SupplierInvoiceItemWriteSchema] = field(default_factory=list)
    purchase_order_id: Optional[int] = None
    due_date: Optional[datetime] = None
    status: InvoiceStatusEnum = InvoiceStatusEnum.UNPAID
    payment_status: PaymentStatusEnum = PaymentStatusEnum.PENDING
    subtotal: Decimal = Decimal("0.00")
    other_charges: Decimal = Decimal("0.00")
    discount_amount: Decimal = Decimal("0.00")
    amount_paid: Decimal = Decimal("0.00")
    currency: str = "USD"
    notes: Optional[str] = None
