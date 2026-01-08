from litestar import Router, get, post, put, delete, Controller


class SupplierInvoiceController(Controller):
    path = "/supplier_invoices"

    @get("/")
    async def list_invoices(self):
        return {"message": "List of supplier invoices"}

    @post("/")
    async def create_invoice(self):
        return {"message": "Supplier invoice created"}

    @get("/{invoice_id}")
    async def get_invoice(self, invoice_id: int):
        return {"message": f"Details of supplier invoice {invoice_id}"}

    @put("/{invoice_id}")
    async def update_invoice(self, invoice_id: int):
        return {"message": f"Supplier invoice {invoice_id} updated"}

    @delete("/{invoice_id}")
    async def delete_invoice(self, invoice_id: int):
        return {"message": f"Supplier invoice {invoice_id} deleted"}