from enum import Enum
from io import StringIO
from fastapi import FastAPI, File
from fastapi.testclient import TestClient
from csv import DictReader
from pathlib import Path

app = FastAPI()


@app.post("/product/top")
async def get_top_product(file: bytes = File(...)):
    csv_fo = StringIO(file.decode("utf-8"))
    r = DictReader(csv_fo)
    max_product = Product()

    for row in r:
        # Validate CSV Schema
        if not all(k in row.keys() for k in ('id', 'product_name', 'customer_average_rating')):
            return TopProductResponse(None, None, False, Errors.CSV_WRONG_SCHEMA)

        # Validate id column type
        try:
            int(row['id'])
        except:
            return TopProductResponse(None, None, False, Errors.ID_NOT_INT)

        # Validate product_name column len
        if len(row['product_name']) < 1:
            return TopProductResponse(None, None, False, Errors.PRODUCT_NAME_EMPTY)

        # Validate customer_average_rating column type
        try:
            float(row['customer_average_rating'])
        except:
            return TopProductResponse(None, None, False, Errors.CUSTOMER_AVERAGE_RATING_NOT_FLOAT)

        if float(row['customer_average_rating']) > max_product.rating:
            max_product.id = int(row['id'])
            max_product.name = row['product_name']
            max_product.rating = float(row['customer_average_rating'])

    return TopProductResponse(max_product.name, max_product.rating, True, None)


# Classes
class Product:
    def __init__(self, id: int = 1, name: str = "", rating: float = -1):
        self.id = id
        self.name = name
        self.rating = rating


class TopProductResponse:
    def __init__(self, top_product: str, product_rating: float, is_successful: bool, error: str):
        self.top_product = top_product
        self.product_rating = product_rating
        self.is_successful = is_successful
        self.error = error

# Enums


class Errors(str, Enum):
    def __str__(self):
        return str(self.value)
    CSV_WRONG_SCHEMA = 'CSV Provided Schema is incorrect.'
    ID_NOT_INT = 'id value is not an integer'
    PRODUCT_NAME_EMPTY = 'product_name is empty'
    CUSTOMER_AVERAGE_RATING_NOT_FLOAT = 'customer_average_rating value is not a float'


# Tests
client = TestClient(app)

def test_get_top_product():
    response = client.post(
        "/product/top", files={"file": ("resal.csv", open(
            Path.joinpath(Path(__file__).parent.resolve(),
                          "resal.csv"), "rb"), "text/csv")}
    )
    assert response.status_code == 200
    assert response.json() == {
        "top_product": "Massoub gift card",
        "product_rating": 5.0,
        "is_successful": True,
        "error": None
    }


def test_get_top_product_wrong_schema():
    response = client.post(
        "/product/top", files={"file": ("resal_wrong.csv", open(
            Path.joinpath(Path(__file__).parent.resolve(),
                          "resal_wrong.csv"), "rb"), "text/csv")}
    )
    assert response.status_code == 200
    assert response.json() == {
        "top_product": None,
        "product_rating": None,
        "is_successful": False,
        "error": "CSV Provided Schema is incorrect."
    }


def test_get_top_product_wrong_id():
    response = client.post(
        "/product/top", files={"file": ("resal_wrong_id.csv", open(
            Path.joinpath(Path(__file__).parent.resolve(),
                          "resal_wrong_id.csv"), "rb"), "text/csv")}
    )
    assert response.status_code == 200
    assert response.json() == {
        "top_product": None,
        "product_rating": None,
        "is_successful": False,
        "error": Errors.ID_NOT_INT
    }


def test_get_top_product_wrong_name():
    response = client.post(
        "/product/top", files={"file": ("resal_wrong_name.csv", open(
            Path.joinpath(Path(__file__).parent.resolve(),
                          "resal_wrong_name.csv"), "rb"), "text/csv")}
    )
    assert response.status_code == 200
    assert response.json() == {
        "top_product": None,
        "product_rating": None,
        "is_successful": False,
        "error": Errors.PRODUCT_NAME_EMPTY
    }


def test_get_top_product_wrong_rating():
    response = client.post(
        "/product/top", files={"file": ("resal_wrong_rating.csv", open(
            Path.joinpath(Path(__file__).parent.resolve(),
                          "resal_wrong_rating.csv"), "rb"), "text/csv")}
    )
    assert response.status_code == 200
    assert response.json() == {
        "top_product": None,
        "product_rating": None,
        "is_successful": False,
        "error": Errors.CUSTOMER_AVERAGE_RATING_NOT_FLOAT
    }
