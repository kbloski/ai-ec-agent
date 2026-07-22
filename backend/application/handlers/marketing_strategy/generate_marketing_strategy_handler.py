import json

from di.container import Container
from domain.models.ollama.llm_ollama_message import LlmOllamaMessage
from domain.enums.ollama_message_role import OllamaMessageRole
from domain.models.marketing_strategy.marketing_strategy import MarketingStrategy


SYSTEM_PROMPT = """
You are an expert in marketing strategy and growth marketing.

Your task is to create a marketing strategy based on the available context.

Your goal is to define:

- how to acquire customers,
- which channels to use,
- what the customer journey looks like,
- what marketing activities should be performed,
- how to build trust,
- which segments should be prioritized,
- which hypotheses should be tested.


Do not generate:
- advertisements,
- headlines,
- sales copy,
- landing pages,
- emails,
- creative assets.


Return only valid JSON:

{
    "marketing_objective": "",
    "growth_strategy": "",

    "primary_audience": [""],

    "secondary_audience": [""],

    "audience_prioritization": [
        {
            "audience": "",
            "reason": "",
            "potential": ""
        }
    ],

    "customer_journey": {
        "awareness": "",
        "consideration": "",
        "conversion": "",
        "retention": ""
    },

    "marketing_channels": [
        {
            "channel": "",
            "role": "",
            "strategy": ""
        }
    ],

    "acquisition_strategy": [""],

    "trust_building_strategy": [""],

    "content_strategy": {
        "main_pillars": [""],
        "content_goals": [""]
    },

    "community_strategy": [""],

    "creator_influencer_strategy": [""],

    "campaign_directions": [
        {
            "name": "",
            "objective": "",
            "audience": "",
            "strategic_angle": ""
        }
    ],

    "conversion_strategy": [""],

    "retention_strategy": [""],

    "marketing_experiments": [
        {
            "hypothesis": "",
            "area": "",
            "success_metric": ""
        }
    ],

    "marketing_kpis": [""]
}

Return valid JSON only.
"""

USER_PROMPT_TEMPLATE = """
Generate a marketing strategy based on the following data.

KNOWLEDGE BASE:

{knowledge_json}

BRAND STRATEGY:

{brand_strategy_json}
"""

# To na razie jest w knowledge 
# CUSTOMER & MARKET INSIGHTS:
# {insights_json}



def generate_marketing_strategy_handler(
    knowledge_id: int,
    brand_markeging_id: int
):
    container = Container()

    knowledge_service = container.knowledge_service()
    brand_marketing_service = container.brand_marketing_service()
    ollama_service = container.ollama_service()
    marketing_strategy_repository = container.marketing_strategy_repository()
    marketing_strategy_service = container.marketing_strategy_service()


    knowledge = knowledge_service.get_knowledge_details_by_id(
        knowledge_id=knowledge_id
    )

    brand_strategy = brand_marketing_service.get_brand_marketing_by_id(
        id=brand_markeging_id
    )


    knowledge_json = json.dumps(
        knowledge.to_dict(),
        ensure_ascii=False,
        indent=2,
        default=str
    )

    brand_strategy_json = json.dumps(
        brand_strategy.to_dict(),
        ensure_ascii=False,
        indent=2,
        default=str
    )


    user_prompt = USER_PROMPT_TEMPLATE.format(
        knowledge_json=knowledge_json,
        brand_strategy_json=brand_strategy_json
    )


    response = ollama_service.chat_llm(
        messages=[
            LlmOllamaMessage(
                role=OllamaMessageRole.SYSTEM,
                content=SYSTEM_PROMPT
            ),
            LlmOllamaMessage(
                role=OllamaMessageRole.USER,
                content=user_prompt
            )
        ]
    )


    data = json.loads(response.content.strip())

    entity = MarketingStrategy(
        brand_marketing_id=brand_markeging_id,
        marketing_objective=data.get("marketing_objective"),
        growth_strategy=data.get("growth_strategy"),
        primary_audience=data.get("primary_audience", []),
        secondary_audience=data.get("secondary_audience", []),
        audience_prioritization=data.get("audience_prioritization", []),
        customer_journey=data.get("customer_journey", {}),
        marketing_channels=data.get("marketing_channels", []),
        acquisition_strategy=data.get("acquisition_strategy", []),
        trust_building_strategy=data.get("trust_building_strategy", []),
        content_strategy=data.get("content_strategy", {}),
        community_strategy=data.get("community_strategy", []),
        creator_influencer_strategy=data.get("creator_influencer_strategy", []),
        campaign_directions=data.get("campaign_directions", []),
        conversion_strategy=data.get("conversion_strategy", []),
        retention_strategy=data.get("retention_strategy", []),
        marketing_experiments=data.get("marketing_experiments", []),
        marketing_kpis=data.get("marketing_kpis", []),
    )
    created = marketing_strategy_repository.create(entity)

    return marketing_strategy_service.get_marketing_strategy_by_id(id=created.id)