from fastapi import APIRouter

from application.handlers.offers.get_offers import get_offers
from application.handlers.offers.seed_full_offer import seed_full_offer


def register_offers_routes(router: APIRouter):
    @router.get("/offers")
    def offers(page: int = 1):
        return get_offers( page=page )
        
    
    @router.get("/offers/seed-full")
    def seed_full(page: int = 1):
        return seed_full_offer()


    # @router.get("/products/{product_id}/analyze")
    # def product_analyze(product_id: int):
    #     container = Container()
    #     product_service = container.product_service()

    #     analyze_result = product_service.analyze_product(product_id)

    #     return analyze_result
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