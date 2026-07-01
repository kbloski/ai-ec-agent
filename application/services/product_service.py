from infrastructure.logging.logger import Logger

class ProductService:
    def __init__(self, logger : Logger ):
        # per-instance storage (ważne!)
        self.logger = logger
    
    # def analize_product(
    #         self, 
    #         product_data: dict
    #     ) -> dict:
    #     # Implement your product analysis logic here
    #     self.logger.info("Analyzing product data...")
    #     # For demonstration purposes, let's just return the input data
    #     return {
    #         "status": "success",
    #         "data": product_data
    #     }

