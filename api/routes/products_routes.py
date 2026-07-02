from fastapi import APIRouter
from sqlalchemy import Column
from di.container import Container
from domain.models.ollama.ollama_message import OllamaMessage
from domain.enums.ollama.ollama_message_role import OllamaMessageRole
from domain.models.product.product import Product
import json

from application.handlers.products.get_products import get_products


def register_products_routes(router: APIRouter):
    @router.get("/products")
    def get_all_products(page: int = 1):
        return get_products( page=page )
        
    # @router.get("/products/{id}/delete")
    # def delete_all_products(id : str):
    #     deleted_count = 0
    #     if (id == "all") :
    #         container = Container()
    #         product_repository = container.product_repository()
    #         deleted_count = product_repository.delete_all()
    #     else:
    #         return "Not implemented yet"

    #     return {
    #         "deleted_count": deleted_count
    #     }





    # @router.get("/products/{product_id}/analyze")
    # def product_analyze(product_id: int):
    #     container = Container()
    #     product_service = container.product_service()

    #     analyze_result = product_service.analyze_product(product_id)

    #     return analyze_result