from pathlib import Path
from fastapi.testclient import TestClient
from app.main import app
from app.enums.errors import Errors

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
        "error": Errors.CSV_WRONG_SCHEMA
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
