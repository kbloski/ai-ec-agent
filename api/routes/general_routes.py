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
from application.handlers.brand_marketing.generate_brand_marketing_handler import generate_brand_marketing_handler
from application.handlers.brand_marketing.get_brand_marketing_handler import get_brand_marketing_handler
from application.handlers.brand_marketing.get_knowledge_brand_marketings_handler import get_knowledge_brand_marketings_handler
from application.handlers.marketing_strategy.generate_marketing_strategy_handler import generate_marketing_strategy_handler
from application.handlers.marketing_strategy.get_marketing_strategy_handler import get_marketing_strategy_handler
from application.handlers.marketing_strategy.get_brand_marketing_marketing_strategies_handler import get_brand_marketing_marketing_strategies_handler
from application.handlers.offer_strategy.generate_offer_strategy_handler import generate_offer_strategy_handler
from application.handlers.offer_strategy.get_offer_strategy_handler import get_offer_strategy_handler
from application.handlers.offer_strategy.get_marketing_strategy_offer_strategies_handler import get_marketing_strategy_offer_strategies_handler
from application.handlers.message_strategy.generate_message_strategy_handler import generate_message_strategy_handler
from application.handlers.message_strategy.get_message_strategy_handler import get_message_strategy_handler
from application.handlers.message_strategy.get_offer_strategy_message_strategies_handler import get_offer_strategy_message_strategies_handler
from application.handlers.page_strategy.generate_page_strategy_json_handler import generate_page_strategy_json_handler
from application.handlers.ad_strategy.generate_ad_strategy_handler import generate_ad_strategy_handler
from application.handlers.ad_strategy.get_ad_strategy_handler import get_ad_strategy_handler
from application.handlers.ad_strategy.get_message_strategy_ad_strategies_handler import get_message_strategy_ad_strategies_handler
from application.handlers.creative_strategy.generate_creative_strategy_handler import generate_creative_strategy_handler
from application.handlers.ad_execution.generate_ad_execution_handler import generate_ad_execution_handler
from application.handlers.ad_execution.get_ad_execution_handler import get_ad_execution_handler
from application.handlers.ad_execution.get_creative_strategy_ad_executions_handler import get_creative_strategy_ad_executions_handler
from application.handlers.creative_strategy.get_creative_strategy_handler import get_creative_strategy_handler
from application.handlers.creative_strategy.get_ad_strategy_creative_strategies_handler import get_ad_strategy_creative_strategies_handler


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

    @router.get("/brand-marketing/{brand_marketing_id}/marketing-strategy")
    def get_brand_marketing_marketing_strategies( brand_marketing_id: int ):
        return get_brand_marketing_marketing_strategies_handler( brand_marketing_id=brand_marketing_id )

    @router.get("/marketing-strategy/{id}")
    def get_marketing_strategy( id: int ):
        return get_marketing_strategy_handler( id=id )


    # -----------------------------
    # Offer strategy
    # -----------------------------
    @router.get("/knowledges/{knowledge_id}/brand-marketing/{brand_marketing_id}/marketing-strategy/{marketing_strategy_id}/offer-strategy/generate")
    def knowledge_offer_strategy_generate( knowledge_id: int, brand_marketing_id: int, marketing_strategy_id: int ):
        return generate_offer_strategy_handler(
            knowledge_id=knowledge_id,
            brand_marketing_id=brand_marketing_id,
            marketing_strategy_id=marketing_strategy_id
        )

    @router.get("/marketing-strategy/{marketing_strategy_id}/offer-strategy")
    def get_marketing_strategy_offer_strategies( marketing_strategy_id: int ):
        return get_marketing_strategy_offer_strategies_handler( marketing_strategy_id=marketing_strategy_id )

    @router.get("/offer-strategy/{id}")
    def get_offer_strategy( id: int ):
        return get_offer_strategy_handler( id=id )


    # -----------------------------
    # Message strategy
    # -----------------------------
    @router.get("/knowledges/{knowledge_id}/brand-marketing/{brand_marketing_id}/marketing-strategy/{marketing_strategy_id}/offer-strategy/{offer_strategy_id}/message-strategy/generate")
    def knowledge_message_strategy_generate( knowledge_id: int, brand_marketing_id: int, marketing_strategy_id: int, offer_strategy_id: int ):
        return generate_message_strategy_handler(
            knowledge_id=knowledge_id,
            brand_marketing_id=brand_marketing_id,
            marketing_strategy_id=marketing_strategy_id,
            offer_strategy_id=offer_strategy_id
        )

    @router.get("/offer-strategy/{offer_strategy_id}/message-strategy")
    def get_offer_strategy_message_strategies( offer_strategy_id: int ):
        return get_offer_strategy_message_strategies_handler( offer_strategy_id=offer_strategy_id )

    @router.get("/message-strategy/{id}")
    def get_message_strategy( id: int ):
        return get_message_strategy_handler( id=id )


    # -----------------------------
    # Ad strategy
    # -----------------------------
    @router.get("/knowledges/{knowledge_id}/brand-marketing/{brand_marketing_id}/marketing-strategy/{marketing_strategy_id}/offer-strategy/{offer_strategy_id}/message-strategy/{message_strategy_id}/ad-strategy/generate")
    def knowledge_ad_strategy_generate( knowledge_id: int, brand_marketing_id: int, marketing_strategy_id: int, offer_strategy_id: int, message_strategy_id: int ):
        return generate_ad_strategy_handler(
            knowledge_id=knowledge_id,
            brand_marketing_id=brand_marketing_id,
            marketing_strategy_id=marketing_strategy_id,
            offer_strategy_id=offer_strategy_id,
            message_strategy_id=message_strategy_id
        )

    @router.get("/message-strategy/{message_strategy_id}/ad-strategy")
    def get_message_strategy_ad_strategies( message_strategy_id: int ):
        return get_message_strategy_ad_strategies_handler( message_strategy_id=message_strategy_id )

    @router.get("/ad-strategy/{id}")
    def get_ad_strategy( id: int ):
        return get_ad_strategy_handler( id=id )


    # -----------------------------
    # Creative strategy
    # -----------------------------
    @router.get("/knowledges/{knowledge_id}/brand-marketing/{brand_marketing_id}/marketing-strategy/{marketing_strategy_id}/offer-strategy/{offer_strategy_id}/message-strategy/{message_strategy_id}/ad-strategy/{ad_strategy_id}/creative-strategy/generate")
    def knowledge_creative_strategy_generate( knowledge_id: int, brand_marketing_id: int, marketing_strategy_id: int, offer_strategy_id: int, message_strategy_id: int, ad_strategy_id: int ):
        return generate_creative_strategy_handler(
            knowledge_id=knowledge_id,
            brand_marketing_id=brand_marketing_id,
            marketing_strategy_id=marketing_strategy_id,
            offer_strategy_id=offer_strategy_id,
            message_strategy_id=message_strategy_id,
            ad_strategy_id=ad_strategy_id
        )

    @router.get("/ad-strategy/{ad_strategy_id}/creative-strategy")
    def get_ad_strategy_creative_strategies( ad_strategy_id: int ):
        return get_ad_strategy_creative_strategies_handler( ad_strategy_id=ad_strategy_id )

    @router.get("/creative-strategy/{id}")
    def get_creative_strategy( id: int ):
        return get_creative_strategy_handler( id=id )


    # -----------------------------
    # Ad execution
    # -----------------------------
    @router.get("/knowledges/{knowledge_id}/brand-marketing/{brand_marketing_id}/marketing-strategy/{marketing_strategy_id}/offer-strategy/{offer_strategy_id}/message-strategy/{message_strategy_id}/ad-strategy/{ad_strategy_id}/creative-strategy/{creative_strategy_id}/ad-execution/generate")
    def creative_strategy_ad_execution_generate( knowledge_id: int, brand_marketing_id: int, marketing_strategy_id: int, offer_strategy_id: int, message_strategy_id: int, ad_strategy_id: int, creative_strategy_id: int ):
        return generate_ad_execution_handler(
            knowledge_id=knowledge_id,
            brand_marketing_id=brand_marketing_id,
            marketing_strategy_id=marketing_strategy_id,
            offer_strategy_id=offer_strategy_id,
            message_strategy_id=message_strategy_id,
            ad_strategy_id=ad_strategy_id,
            creative_strategy_id=creative_strategy_id
        )

    @router.get("/creative-strategy/{creative_strategy_id}/ad-execution")
    def get_creative_strategy_ad_executions( creative_strategy_id: int ):
        return get_creative_strategy_ad_executions_handler( creative_strategy_id=creative_strategy_id )

    @router.get("/ad-execution/{id}")
    def get_ad_execution( id: int ):
        return get_ad_execution_handler( id=id )


    # -----------------------------
    # Page strategy
    # -----------------------------
    @router.get("/knowledges/{knowledge_id}/brand-marketing/{brand_marketing_id}/marketing-strategy/{marketing_strategy_id}/offer-strategy/{offer_strategy_id}/message-strategy/{message_strategy_id}/page-strategy/generate")
    def knowledge_page_strategy_generate( knowledge_id: int, brand_marketing_id: int, marketing_strategy_id: int, offer_strategy_id: int, message_strategy_id: int ):
        return generate_page_strategy_json_handler(
            knowledge_id=knowledge_id,
            message_strategy_id=message_strategy_id,
            brand_marketing_id=brand_marketing_id,
            marketing_strategy_id=marketing_strategy_id,
            offer_strategy_id=offer_strategy_id
        )


    # -----------------------------
    # Knowledges advertisement
    # -----------------------------
    # @router.get("/knowledges/{knowledge_id}/advertisements/generate")
    # def knowledge_advertisement_generate( knowledge_id : int, count: int = 3 ):
    #     return knowledge_advertisement_generate_handler( knowledge_id=knowledge_id, count=count )
