from fastapi import APIRouter
from sqlalchemy import Column

from di.container import Container
from domain.models.ollama.ollama_message import OllamaMessage
from domain.enums.ollama.ollama_message_role import OllamaMessageRole
from domain.models.product.product import Product
import json

def register_product_routes(router: APIRouter):
    @router.get("/products/delete")
    def delete_all_products():
        container = Container()
        product_repository = container.product_repository()

        deleted_count = product_repository.delete_all()
        return {"deleted_count": deleted_count}

    @router.get("/products")
    def get_all_products():
        container = Container()
        product_repository = container.product_repository()

        products = product_repository.get_all()
        return products


    @router.get("/products/add")
    def add_product():
        container = Container()
        product_repository = container.product_repository()

        product = Product(
            name="Prosty blender kuchenny",
            buying_price=120,
            description="Blender do robienia smoothie i jedzenia. Czasem działa szybko, czasem wolno.",
            target_audience=[
                "ludzie, którzy nie lubią gotować",
                "studenci",
                "osoby zmęczone po pracy",
                "osoby, które chcą jeść zdrowiej"
            ],
            pain_points=[
                "brak czasu na gotowanie",
                "nie chce się myć wielu naczyń",
                "chęć szybkiego jedzenia",
                "brak pomysłów co zjeść",
                "zmęczenie po całym dniu"
            ]
        )

        product = product_repository.create(product)

        return product


    @router.get("/products/{product_id}/analyze")
    def product_analyze(product_id: int):
        container = Container()
        product_service = container.product_service()

        analyze_result = product_service.analyze_product(product_id)

        return analyze_result