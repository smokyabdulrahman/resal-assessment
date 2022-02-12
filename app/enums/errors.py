from enum import Enum

class Errors(str, Enum):
    def __str__(self):
        return str(self.value)
    CSV_WRONG_SCHEMA = 'CSV Provided Schema is incorrect.'
    ID_NOT_INT = 'id value is not an integer'
    PRODUCT_NAME_EMPTY = 'product_name is empty'
    CUSTOMER_AVERAGE_RATING_NOT_FLOAT = 'customer_average_rating value is not a float'