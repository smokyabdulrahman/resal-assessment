class TopProductDto:
    def __init__(self, top_product: str, product_rating: float, is_successful: bool, error: str):
        self.top_product = top_product
        self.product_rating = product_rating
        self.is_successful = is_successful
        self.error = error