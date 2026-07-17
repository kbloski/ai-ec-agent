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
from application.handlers.checklist.get_checklist_by_id_handler import get_checklist_by_id_handler
from application.handlers.advertisement.knowledge_advertisement_generate_handler import knowledge_advertisement_generate_handler
from application.handlers.advertisement.get_advertisements_handler import get_advertisements_handler
from application.handlers.advertisement.get_advertisement_handler import get_advertisement_handler
from application.handlers.sales_assets.generate_sales_asset_handler import generate_sales_asset_handler
from application.handlers.sales_assets.get_sales_assets_handler import get_sales_assets_handler
from application.handlers.sales_assets.get_sales_asset_handler import get_sales_asset_handler
from application.handlers.experiments.knowledge_experiments_generate_handler import knowledge_experiments_generate_handler
from application.handlers.experiments.get_knowledge_experiments_handler import get_knowledge_experiments_handler
from application.handlers.experiments.get_knowledge_experiment_handler import get_knowledge_experiment_handler
from application.handlers.brand_marketing.generate_brand_marketing_handler import generate_brand_marketing_handler
from application.handlers.brand_marketing.get_brand_marketing_handler import get_brand_marketing_handler
from application.handlers.brand_marketing.get_knowledge_brand_marketings_handler import get_knowledge_brand_marketings_handler
from application.handlers.marketing_strategy.generate_marketing_strategy_handler import generate_marketing_strategy_handler


def register_general_routes(router: APIRouter):

    
    # -----------------------------
    # Offers
    # -----------------------------

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



    # -----------------------------
    # Knowledges
    # -----------------------------

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



    # -----------------------------
    # Target audience
    # -----------------------------

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



    # -----------------------------
    # Checklist 
    # -----------------------------
    @router.get("/checklists/{checklist_id}")
    def get_checklist_for_analysis( checklist_id: int):
        return get_checklist_by_id_handler( checklist_id=checklist_id)  

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



    # -----------------------------
    # Brand marketing
    # -----------------------------
    @router.get("/knowledges/{knowledge_id}/brand-marketing/generate")
    def knowledge_brand_marketing_generate( knowledge_id: int ):
        return generate_brand_marketing_handler( knowledge_id=knowledge_id )

    @router.get("/knowledges/{knowledge_id}/brand-marketing")
    def get_knowledge_brand_marketing( knowledge_id: int ):
        return get_knowledge_brand_marketings_handler( knowledge_id=knowledge_id )

    @router.get("/brand-marketing/{id}")
    def get_brand_marketing( id: int ):
        return get_brand_marketing_handler( id=id )


    # -----------------------------
    # Marketing strategy
    # -----------------------------
    @router.get("/knowledges/{knowledge_id}/brand-marketing/{brand_markeging_id}/marketing-strategy/generate")
    def knowledge_marketing_strategy_generate( knowledge_id: int, brand_markeging_id: int ):
        return generate_marketing_strategy_handler( knowledge_id=knowledge_id, brand_markeging_id=brand_markeging_id )
    
    
    
    
    
    
    

    # -----------------------------
    # Sales assets
    # -----------------------------
    # @router.get("/knowledges/{knowledge_id}/sales-assets/generate")
    # def knowledge_sales_asset_generate(knowledge_id: int, type: str = "landing_page"):
    #     return generate_sales_asset_handler(knowledge_id=knowledge_id, type=type)

    # @router.get("/knowledges/{knowledge_id}/sales-assets")
    # def get_knowledge_sales_assets(knowledge_id: int):
    #     return get_sales_assets_handler(knowledge_id=knowledge_id)

    # @router.get("/sales-assets/{id}")
    # def get_sales_asset(id: int):
    #     return get_sales_asset_handler(id=id)


    # -----------------------------
    # Knowledges advertisement
    # -----------------------------
    # @router.get("/knowledges/{knowledge_id}/advertisements/generate")
    # def knowledge_advertisement_generate( knowledge_id : int, count: int = 3 ):
    #     return knowledge_advertisement_generate_handler( knowledge_id=knowledge_id, count=count )

    # @router.get("/knowledges/{knowledge_id}/advertisements")
    # def get_knowledge_advertisements( knowledge_id: int ):
    #     return get_advertisements_handler( knowledge_id=knowledge_id )

    # @router.get("/advertisements/{id}")
    # def get_advertisement( id: int ):
    #     return get_advertisement_handler( id=id )


    # -----------------------------
    # Knowledges experiments
    # -----------------------------
    # @router.get("/knowledges/{knowledge_id}/experiments/generate")
    # def knowledge_experiments_generate( knowledge_id: int, count: int = 10 ):
    #     return knowledge_experiments_generate_handler( knowledge_id=knowledge_id, count=count )

    # @router.get("/knowledges/{knowledge_id}/experiments")
    # def get_knowledge_experiments( knowledge_id: int ):
    #     return get_knowledge_experiments_handler( knowledge_id=knowledge_id )

    # @router.get("/experiments/{id}")
    # def get_knowledge_experiment( id: int ):
    #     return get_knowledge_experiment_handler( id=id )
