from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass
class SupplierReadSchema:
    id: int
    name: str
    company_name: Optional[str]
    contact_person: Optional[str]
    email: Optional[str]
    phone: Optional[str]
    mobile: Optional[str]
    website: Optional[str]
    address_line1: Optional[str]
    city: Optional[str]
    country: Optional[str]
    currency: str
    is_active: bool
    notes: Optional[str]
    created_at: datetime
    updated_at: datetime


@dataclass
class SupplierWriteSchema:
    name: str
    company_name: Optional[str] = None
    contact_person: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    mobile: Optional[str] = None
    website: Optional[str] = None
    address_line1: Optional[str] = None
    city: Optional[str] = None
    country: Optional[str] = None
    currency: str = "USD"
    is_active: bool = True
    notes: Optional[str] = None