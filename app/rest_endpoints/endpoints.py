from app.main import app
from io import StringIO
from fastapi import File
from app.services import product_service

@app.post("/product/top")
async def get_top_product(file: bytes = File(...)):
    csv_file = StringIO(file.decode("utf-8"))
    res = product_service.process_top_product(csv_file)

    return res