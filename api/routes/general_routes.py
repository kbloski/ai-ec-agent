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
from application.handlers.analysis.knowledge_analysis_answers_generate_handler import knowledge_analysis_answers_generate_handler
from application.handlers.analysis.create_analysis_for_knowledge_handler import create_analysis_for_knowledge_handler
from application.handlers.analysis.get_analysis_by_id_hanlder import get_analysis_by_id_handler
from application.handlers.analysis.get_analysis_for_knowledge_hanlder import get_analysis_for_knowledge_handler
from application.handlers.analysis.analyse_checklist_generate_handler import analyse_checklist_generate_handler
from application.handlers.checklist.create_checklist_for_analysis_handler import create_checklist_for_analysis_handler
from application.handlers.checklist.get_analysis_checklists_handler import get_analyse_checklists_handler




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
    # POST in future 
    @router.get("/analysis/{analyse_id}")
    def get_anlysis_by_id(analyse_id: int):
        return get_analysis_by_id_handler( analyse_id=analyse_id)

    @router.get("/knowledges/{knowledge_id}/analysis/create")
    def create_analysis_for_knowledge(knowledge_id: int):
        return create_analysis_for_knowledge_handler(knowledge_id=knowledge_id)

    @router.get("/knowledges/{knowledge_id}/analysis")
    def get_analysis_for_knowledge(knowledge_id: int):
        return get_analysis_for_knowledge_handler(knowledge_id=knowledge_id)

    # POST in future 
    @router.get("/knowledges/{knowledge_id}/analysis/{analyse_id}/answers/generate")
    def knowledge_analysis_answers_generate(knowledge_id: int, analyse_id: int):
        return knowledge_analysis_answers_generate_handler( knowledge_id=knowledge_id, analyse_id=analyse_id)

    @router.get("/knowledges/{knowledge_id}/analysis/{analysis_id}/checklists/create")
    def create_analyse_checklist(knowledge_id: int, analysis_id: int):
        return create_checklist_for_analysis_handler( analysis_id=analysis_id)  

    # POST in future 
    @router.get("/knowledges/{knowledge_id}/analysis/{analyse_id}/checklists/{checklist_id}/generate")
    def analyse_checklist_generate(knowledge_id: int, analyse_id: int, checklist_id: int):
        return analyse_checklist_generate_handler( knowledge_id=knowledge_id, analyse_id=analyse_id, checklist_id=checklist_id)

    @router.get("/analysis/{analysis_id}/checklists")
    def get_checklist_for_analysis( analysis_id: int):
        return get_analyse_checklists_handler( analyse_id=analysis_id)  