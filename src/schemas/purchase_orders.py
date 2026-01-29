from dataclasses import dataclass, field
from datetime import datetime
from decimal import Decimal
from enum import Enum
from typing import Optional


class PurchaseOrderStatus(str, Enum):
    DRAFT = "DRAFT"
    SENT = "SENT"
    APPROVED = "APPROVED"
    PARTIALLY_RECEIVED = "PARTIALLY_RECEIVED"
    COMPLETED = "COMPLETED"
    CANCELLED = "CANCELLED"


@dataclass
class PurchaseOrderReadSchema:
    po_number: str
    supplier_id: int
    order_date: datetime
    expected_delivery_date: Optional[datetime]
    status: PurchaseOrderStatus
    subtotal: Decimal
    discount_amount: Decimal
    total_amount: Decimal
    paid_amount: Decimal
    notes: Optional[str]
    created_at: datetime
    updated_at: datetime
    id: Optional[int] = None


@dataclass
class PurchaseOrderWriteSchema:
    po_number: str
    supplier_id: int
    items: list["PurchaseOrderItemWriteSchema"]
    order_date: datetime = field(default_factory=datetime.now)
    total_amount: Decimal = Decimal("0.00")
    expected_delivery_date: Optional[datetime] = None
    status: PurchaseOrderStatus = PurchaseOrderStatus.DRAFT
    subtotal: Decimal = Decimal("0.00")
    discount_amount: Decimal = Decimal("0.00")
    paid_amount: Decimal = Decimal("0.00")
    notes: Optional[str] = None


@dataclass
class PurchaseOrderItemReadSchema:
    purchase_order_id: int
    product_id: int
    quantity_ordered: int
    quantity_received: int
    unit_price: Decimal
    discount_amount: Decimal
    subtotal: Decimal
    notes: Optional[str]
    created_at: datetime
    updated_at: datetime
    id: Optional[int] = None



@dataclass
class PurchaseOrderItemWriteSchema:
    purchase_order_id: int
    product_id: int
    quantity_ordered: int
    unit_price: Decimal
    subtotal: Decimal
    quantity_received: int = 0
    discount_amount: Decimal = Decimal("0.00")
    notes: Optional[str] = None
