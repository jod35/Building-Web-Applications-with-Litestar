import asyncio
import sys
from datetime import datetime, date

from litestar import Litestar
from litestar.testing import TestClient
from advanced_alchemy.extensions.litestar import SQLAlchemyPlugin
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

# Import your app creation logic or main app
# Assuming main.py has the 'app' object or a create_app function.
# Adjusting imports to match user's structure based on available files.
from main import app
from src.db.models import SupplierModel, ProductModel, SupplierInvoiceModel, SupplierInvoiceItemModel
from src.db.repositories import SupplierRepository, ProductRepository, SupplierInvoiceRepository

async def seed_data(session: AsyncSession):
    # Create Supplier
    supplier = SupplierModel(
        name="Test Supplier",
        contact_name="John Doe",
        email="test@example.com",
        phone="1234567890",
        address="123 Test St",
        currency="USD",
        payment_terms="Net 30"
    )
    session.add(supplier)
    await session.flush()

    # Create Product
    product = ProductModel(
        name="Test Product",
        description="A test product",
        sku="TEST-SKU-001",
        category="Test Category",
        unit="pcs",
        unit_price=10.00,
        currency="USD",
        supplier_id=supplier.id
    )
    session.add(product)
    await session.flush()
    
    product2 = ProductModel(
        name="Test Product 2",
        description="Another test product",
        sku="TEST-SKU-002",
        category="Test Category",
        unit="pcs",
        unit_price=20.00,
        currency="USD",
        supplier_id=supplier.id
    )
    session.add(product2)
    await session.flush()

    # Create Supplier Invoice
    invoice = SupplierInvoiceModel(
        invoice_number="INV-001",
        supplier_id=supplier.id,
        invoice_date=date.today(),
        due_date=date.today(),
        status="Unpaid",
        payment_status="Pending",
        total_amount=100.00,
        subtotal=100.00,
        balance_due=100.00,
        currency="USD"
    )
    session.add(invoice)
    await session.flush()
    
    # Add initial items
    item = SupplierInvoiceItemModel(
        invoice_id=invoice.id,
        product_id=product.id,
        quantity=10,
        unit_price=10.00,
        subtotal=100.00
    )
    session.add(item)
    await session.commit()
    
    return supplier.id, product.id, product2.id, invoice.id

def verify_updates():
    with TestClient(app=app) as client:
        # We need to access the database to seed data.
        # Since TestClient spins up the app, we might need a way to insert data first.
        # However, for simplicity in this environment, let's assume we can use the app's db connection 
        # or use a separate script that imports dependencies.
        # But `app` in main.py likely initializes the DB.
        
        # NOTE: This script assumes a running DB or that the app handles it.
        # If this is a real persistent DB, we might pile up garbage data.
        # Ideally we use a testing DB. For now, we will try to rely on the app's behavior.
        pass

async def main():
    # Because setting up a full test environment with TestClient and async DB locally 
    # might be tricky without a full pytest setup, I will attempt to stick to 
    # the existing patterns if possible or use a direct script approach with the app's DI.
    
    # However, running the app directly via UVicorn and hitting it with requests might be easier
    # if I can't easily hook into the DB session here. 
    
    # Let's try to simulate the request flow using TestClient which is synchronous 
    # but communicates with the async app.
    
    with TestClient(app=app) as client:
        # 1. Create resources via API if possible to avoid direct DB hacking
        # Create Supplier
        try:
             # Just checking if we can hit the health check or similar first?
             # Assuming standard routes exist.
             pass
        except Exception as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    # To properly test, I'll rely on generating a pytest file instead.
    # writing a quick test file is safer than a loose script given the async nature + DB.
    pass
