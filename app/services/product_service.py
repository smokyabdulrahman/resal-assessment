from csv import DictReader
from app.dtos.top_product_dto import TopProductDto
from app.enums.errors import Errors
from app.models.product import Product
from io import StringIO

def process_top_product(csv_file: StringIO) -> TopProductDto:
    r = DictReader(csv_file)
    max_product = Product()

    for row in r:
        # Validate CSV Schema
        if not all(k in row.keys() for k in ('id', 'product_name', 'customer_average_rating')):
            return TopProductDto(None, None, False, Errors.CSV_WRONG_SCHEMA)

        # Validate id column type
        try:
            int(row['id'])
        except:
            return TopProductDto(None, None, False, Errors.ID_NOT_INT)

        # Validate product_name column len
        if len(row['product_name']) < 1:
            return TopProductDto(None, None, False, Errors.PRODUCT_NAME_EMPTY)

        # Validate customer_average_rating column type
        try:
            float(row['customer_average_rating'])
        except:
            return TopProductDto(None, None, False, Errors.CUSTOMER_AVERAGE_RATING_NOT_FLOAT)

        if float(row['customer_average_rating']) > max_product.rating:
            max_product.id = int(row['id'])
            max_product.name = row['product_name']
            max_product.rating = float(row['customer_average_rating'])

    return TopProductDto(max_product.name, max_product.rating, True, None)
