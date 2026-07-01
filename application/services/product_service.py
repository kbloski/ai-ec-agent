from infrastructure.logging.logger import Logger
from infrastructure.repositories.products_repository import ProductRepository
from .ollama_service import OllamaService

class ProductService:
    def __init__(self, logger: Logger, product_repository: ProductRepository, ollama_service: OllamaService):
        self.logger = logger
        self.product_repo = product_repository
        self.ollama_service = ollama_service

    def analyze_product(self, product_id: int):
        self.logger.info("Analyzing product data...")

        product = self.product_repo.get_by_id(product_id)
        if not product:
            self.logger.error(f"Product with ID {product_id} not found.")
            return {
                "error": f"Product with ID {product_id} not found."
            }



        return {
            "product": product
        }