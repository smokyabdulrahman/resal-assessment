from io import StringIO
from fastapi import FastAPI, File, UploadFile
from csv import DictReader

app = FastAPI()


@app.post("/product/top")
async def get_top_product(file: bytes = File(...)):
    csv_fo = StringIO(file.decode("utf-8"))
    r = DictReader(csv_fo)
    max_product = Product()
    
    for row in r:
        if float(row['customer_average_rating']) > max_product.rating:
            max_product.id = int(row['id'])
            max_product.name = row['product_name']
            max_product.rating = float(row['customer_average_rating'])

    return {
        "top_product": max_product.name,
        "product_rating": max_product.rating
        }


class Product:
  def __init__(self, id: int = 1, name: str = "", rating: float = -1):
    self.id = id
    self.name = name
    self.rating = rating