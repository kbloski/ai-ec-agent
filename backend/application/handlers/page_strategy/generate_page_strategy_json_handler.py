import json

from di.container import Container
from domain.models.ollama.llm_ollama_message import LlmOllamaMessage
from domain.enums.ollama_message_role import OllamaMessageRole
from domain.models.page_strategy.page_strategy import PageStrategy

SYSTEM_PROMPT = """
You are an expert in:

- Conversion Rate Optimization (CRO)
- Landing Page Strategy
- Customer Psychology
- Direct Response Marketing
- Marketing Strategy
- Consumer Behavior


Your task is to create a PAGE STRATEGY
based on the full marketing context.


Page Strategy defines:

- why the page exists,
- who it is designed for,
- what customer problem it solves,
- what customer beliefs need to change,
- what arguments lead to the purchase decision,
- what purchase barriers need to be removed.


Page Strategy is NOT:

- page structure,
- wireframe,
- landing page section list,
- copywriting,
- UI design,
- HTML/CSS/React.


Do not generate:

- hero section,
- landing page sections,
- headlines,
- slogans,
- CTA copy,
- layouts,
- components.


ANALYSIS:


1. CUSTOMER ANALYSIS

Determine:

- who the most valuable customer is,
- what the customer wants to achieve,
- what problem the customer wants to solve,
- what the customer is afraid of,
- what purchase barriers they have,
- what their main purchase motivators are.


2. POSITIONING

Determine:

- how the product should be positioned,
- what the main product value is,
- why the customer should choose this solution,
- what differentiates the product from alternatives.


3. MESSAGE STRATEGY

Determine:

- the main strategic message,
- the main angle,
- the emotional motivator,
- the rational purchase justification,
- the unique mechanism behind the product.


4. CONVERSION STRATEGY

Determine:

- the main goal of the page,
- the desired user action,
- the biggest conversion driver,
- the biggest conversion barriers,
- the most important objections to resolve.


5. CUSTOMER JOURNEY

Determine:

- customer awareness level,
- customer's current psychological state,
- the journey from problem recognition to purchase decision,
- the most important decision moment.


JSON FORMAT:

{
    "page_strategy": {
        "goal": "",
        "conversion_action": "",

        "target_customer": {
            "description": "",
            "desires": [],
            "problems": [],
            "fears": [],
            "purchase_motivators": []
        },

        "customer_awareness_level": "",
        "customer_journey_stage": "",

        "core_value_proposition": "",
        "main_message": "",
        "message_angle": "",
        "unique_mechanism": "",

        "emotional_drivers": [],
        "rational_drivers": [],

        "purchase_barriers": [],
        "objections_to_resolve": [],

        "trust_requirements": [],

        "competitive_positioning": "",
        "brand_voice_direction": "",

        "conversion_strategy": {
            "primary_conversion_driver": "",
            "secondary_conversion_drivers": [],
            "decision_factors": []
        },

        "customer_journey_strategy": [
            {
                "stage": "",
                "customer_state": "",
                "marketing_goal": ""
            }
        ]
    }
}


RULES:

- Return only valid JSON.
"""


USER_PROMPT_TEMPLATE = """
Generate Page Strategy based on:


KNOWLEDGE BASE:
{knowledge_json}


MESSAGE STRATEGY:
{message_strategy_json}


BRAND STRATEGY:
{brand_strategy_json}


MARKETING STRATEGY:
{marketing_strategy_json}


OFFER STRATEGY:
{offer_strategy_json}
"""


def generate_page_strategy_json_handler(
    knowledge_id: int,
    brand_marketing_id: int,
    marketing_strategy_id: int,
    offer_strategy_id: int,
    message_strategy_id: int
):

    container = Container()


    knowledge_service = container.knowledge_service()
    message_strategy_service = container.message_strategy_service()
    brand_marketing_service = container.brand_marketing_service()
    marketing_strategy_service = container.marketing_strategy_service()
    offer_strategy_service = container.offer_strategy_service()

    page_strategy_repository = container.page_strategy_repository()
    page_strategy_service = container.page_strategy_service()

    ollama_service = container.ollama_service()



    message_strategy = (
        message_strategy_service.get_message_strategy_by_id(
            id=message_strategy_id
        )
    )


    knowledge = (
        knowledge_service.get_knowledge_details_by_id(
            knowledge_id=knowledge_id
        )
    )


    brand_strategy = (
        brand_marketing_service.get_brand_marketing_by_id(
            id=brand_marketing_id
        )
    )


    marketing_strategy = (
        marketing_strategy_service.get_marketing_strategy_by_id(
            id=marketing_strategy_id
        )
    )


    offer_strategy = (
        offer_strategy_service.get_offer_strategy_by_id(
            id=offer_strategy_id
        )
    )



    def serialize(obj):

        return json.dumps(
            obj.to_dict(),
            ensure_ascii=False,
            indent=2,
            default=str
        )



    user_prompt = USER_PROMPT_TEMPLATE.format(

        knowledge_json=serialize(knowledge),

        message_strategy_json=serialize(message_strategy),

        brand_strategy_json=serialize(brand_strategy),

        marketing_strategy_json=serialize(marketing_strategy),

        offer_strategy_json=serialize(offer_strategy)

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



    try:

        content = response.content.strip()


        if content.startswith("```"):

            content = content.replace(
                "```json",
                ""
            )

            content = content.replace(
                "```",
                ""
            ).strip()



        result = json.loads(content)


        if isinstance(result, str):

            result = json.loads(result)



    except Exception:

        return {
            "raw_response": response.content
        }



    page_strategy_data = result.get("page_strategy", {})


    entity = PageStrategy(

        message_strategy_id=message_strategy_id,

        goal=page_strategy_data.get("goal"),

        conversion_action=page_strategy_data.get("conversion_action"),

        target_audience=page_strategy_data.get("target_audience"),

        customer_awareness_level=page_strategy_data.get("customer_awareness_level"),

        customer_journey_stage=page_strategy_data.get("customer_journey_stage"),

        core_value_proposition=page_strategy_data.get("core_value_proposition"),

        main_message=page_strategy_data.get("main_message"),

        message_angle=page_strategy_data.get("message_angle"),

        customer_problem=page_strategy_data.get("customer_problem"),

        customer_desire=page_strategy_data.get("customer_desire"),

        emotional_drivers=page_strategy_data.get("emotional_drivers", []),

        rational_drivers=page_strategy_data.get("rational_drivers", []),

        purchase_motivators=page_strategy_data.get("purchase_motivators", []),

        purchase_barriers=page_strategy_data.get("purchase_barriers", []),

        objections_to_resolve=page_strategy_data.get("objections_to_resolve", []),

        trust_requirements=page_strategy_data.get("trust_requirements", []),

        competitive_positioning=page_strategy_data.get("competitive_positioning"),

        brand_voice_direction=page_strategy_data.get("brand_voice_direction"),

        conversion_strategy=page_strategy_data.get("conversion_strategy"),

        customer_journey_strategy=page_strategy_data.get("customer_journey_strategy", []),

    )


    created = page_strategy_repository.create(entity)


    return page_strategy_service.get_page_strategy_by_id(id=created.id)
