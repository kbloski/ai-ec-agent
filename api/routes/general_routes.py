from fastapi import APIRouter

from application.handlers.offers.get_offers import get_offers
from application.handlers.offers.seed_full_offer import seed_full_offer
from application.handlers.offers.get_offer import get_offer_handler
from application.handlers.offers.offer_knowledge_generate import offer_knowledge_generate_handler
from application.handlers.offers.get_offer_knowledge_handler import get_offer_knowledge_handler
from application.handlers.offers.get_offer_knowledges_handler import get_offer_knowledges_handler
from application.handlers.target_audience.generate_target_audience_handler import generate_target_audience_handler
from application.handlers.target_audience.get_target_audience_handler import get_target_audience_handler
from application.handlers.target_audience.get_target_audience_preview_handler import get_target_audience_preview_handler
from application.handlers.offers.suggest_offer_data_handler import suggets_offer_data_handler
from application.handlers.analysis.generate_knowledge_analysis_handler import generate_knowledge_analysis_handler
from application.handlers.analysis.knowledge_analysis_create_handler import knowledge_analysis_create_handler

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

    
    @router.get("/offers/{id}/suggestions")
    def suggest_offer_data(id: int):
        return suggets_offer_data_handler(offer_id=id)




    # POST in future 
    @router.get("/offers/{id}/knowledges/generate")
    def offer_knowledge_generate(id: int):
        return offer_knowledge_generate_handler(offer_id=id)
    
    #  POST in future 
    @router.get("/offers/{offer_id}/knowledges")
    def get_offer_knowledges(offer_id: int):
        return get_offer_knowledges_handler(offer_id=offer_id)


    #  POST in future 
    @router.get("/knowledges/{knowledge_id}")
    def get_offer_knowledge( knowledge_id : int):
        return get_offer_knowledge_handler( knowledge_id=knowledge_id)





    #  POST in future 
    @router.get("/knowledges/{knowledge_id}/target-audiences/generate")
    def generate_target_audience(knowledge_id: int):
        return generate_target_audience_handler( knowledge_id=knowledge_id)

    # #  GET in future 
    @router.get("/knowledges/{knowledge_id}/target-audiences")
    def get_target_audience( knowledge_id: int):
        return get_target_audience_handler( knowledge_id=knowledge_id)

    # #  GET in future 
    @router.get("/target-audiences/{target_audience_id}")
    def get_target_audience_preview( target_audience_id: int):
        return get_target_audience_preview_handler( target_audience_id=target_audience_id)




    # -----------------------------
    # Analysis
    # -----------------------------

    #  POST in future 
    @router.get("/knowledges/{knowledge_id}/analysis/create")
    def knowledge_analysis_create(knowledge_id: int):
        return knowledge_analysis_create_handler(knowledge_id=knowledge_id)
        # return generate_knowledge_analysis_handler( knowledge_id=knowledge_id)

    # POST in future 
    @router.get("/knowledges/{knowledge_id}/analysis/{analysis_id}/answers/generate")
    def knowledge_analysis_generate(knowledge_id: int):
        return generate_knowledge_analysis_handler( knowledge_id=knowledge_id)