from litestar.plugins.sqlalchemy import BigIntAuditBase
from sqlalchemy import ForeignKey
from sqlalchemy.dialects.mysql import TEXT, VARCHAR
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import Optional

from src.db.models.products import ProductModel
from . import *
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

    def __repr__(self):
        return f"<SupplierModel {self.name}>"

    # relationships
    products: Mapped[list[ProductModel]] = relationship(back_populates="supplier", lazy="selectin")
    supplier_invoices: Mapped[list["SupplierInvoiceModel"]] = relationship(back_populates="supplier", lazy="selectin")
    purchase_orders: Mapped[list["PurchaseOrderModel"]] = relationship(back_populates="supplier", lazy="selectin")