from fastapi import APIRouter

from application.handlers.offers.get_offers import get_offers
from application.handlers.offers.seed_full_offer import seed_full_offer
from application.handlers.offers.get_offer import get_offer_handler
from application.handlers.offers.offer_knowledge_generate import offer_knowledge_generate_handler
from application.handlers.offers.get_offer_knowledge_handler import get_offer_knowledge_handler
from application.handlers.offers.get_offer_knowledges_handler import get_offer_knowledges_handler
from application.handlers.analysis.generate_knowledge_analysis_handler import generate_knowledge_analysis_guides_handler
from application.handlers.analysis.generate_knowledge_analysis_guides_handler import generate_knowledge_analysis_handler

def register_general_routes(router: APIRouter):
    @router.get("/offers")
    def offers(page: int = 1):
        return get_offers( page=page )
        
    @router.get("/offers/seed-full")
    def seed_full(page: int = 1):
        return seed_full_offer()

    @router.get("/offers/{id}")
    def get_offer_details(id: int):
        return get_offer_handler(id=id)
    
    # POST in future 
    @router.get("/offers/{id}/knowledges/generate")
    def offer_knowledge_generate(id: int):
        return offer_knowledge_generate_handler(offer_id=id)
    
    #  POST in future 
    @router.get("/offers/{offer_id}/knowledges")
    def get_offer_knowledges(offer_id: int):
        return get_offer_knowledges_handler(offer_id=offer_id)


    #  POST in future 
    @router.get("/offers/{offer_id}/knowledges/{knowledge_id}")
    def get_offer_knowledge(offer_id: int, knowledge_id : int):
        return get_offer_knowledge_handler(offer_id=offer_id, knowledge_id=knowledge_id)

    #  POST in future 
    @router.get("/offers/{offer_id}/knowledges/{knowledge_id}/analysis/generate")
    def generate_knowledge_analysis(offer_id: int, knowledge_id : int):
        return generate_knowledge_analysis_handler(offer_id=offer_id, knowledge_id=knowledge_id)
    
    @router.get("/offers/{offer_id}/knowledges/{knowledge_id}/analysis-guides/generate")
    def generate_knowledge_analysis_guides(offer_id: int, knowledge_id : int):
        return generate_knowledge_analysis_guides_handler(offer_id=offer_id, knowledge_id=knowledge_id)

