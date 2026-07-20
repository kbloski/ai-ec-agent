import json

from di.container import Container
from domain.models.ollama.llm_ollama_message import LlmOllamaMessage
from domain.enums.ollama_message_role import OllamaMessageRole
from domain.models.page_content_plan.page_content_plan import PageContentPlan


SYSTEM_PROMPT = """
Jesteś ekspertem od:

- Landing Page Content Architecture
- Conversion Rate Optimization
- Direct Response Marketing
- Customer Psychology
- Marketing Content Planning


Twoim zadaniem jest stworzenie PAGE CONTENT PLAN
na podstawie:

- Knowledge Base
- Page Strategy
- Page Blueprint
- Message Strategy
- Offer Strategy


Page Content Plan określa:

- co powinno znaleźć się w każdej sekcji landing page,
- jakie informacje należy przekazać,
- jakie argumenty wykorzystać,
- jakie elementy zwiększają konwersję.


Nie tworzysz:

- finalnego copy,
- headline'ów,
- sloganów,
- CTA tekstów,
- HTML,
- CSS,
- React,
- designu,
- obrazów.


Page Content Plan odpowiada na pytanie:

"Jaką treść i argumentację powinna zawierać każda sekcja strony?"



FORMAT JSON:


{
    "page_content_plan": {

        "sections": [

            {
                "order": 1,

                "section_type": "",

                "content_goal": "",

                "customer_question": "",

                "customer_state": "",

                "main_message_direction": "",

                "content_elements": [

                ],

                "key_arguments": [

                ],

                "emotional_points": [

                ],

                "rational_points": [

                ],

                "proof_needed": [

                ],

                "objections_addressed": [

                ],

                "cta_role": "",

                "visual_support_needed": [

                ],

                "notes": ""

            }

        ]

    }
}



ZASADY:


- Każda sekcja musi odpowiadać sekcji z Page Blueprint.
- Nie dodawaj nowych sekcji.
- Nie usuwaj sekcji z Page Blueprint.
- Nie generuj finalnych tekstów.
- Opisuj kierunek komunikacji.
- Nie twórz gotowych reklam.
- Nie używaj null.
- Wszystkie pola muszą istnieć.


Zwróć wyłącznie JSON.

Bez markdown.

Bez komentarzy.

Tylko JSON.
"""


USER_PROMPT_TEMPLATE = """
Wygeneruj Page Content Plan na podstawie:


KNOWLEDGE BASE:

{knowledge_json}


BRAND MARKETING:

{brand_marketing_json}


MARKETING STRATEGY:

{marketing_strategy_json}


PAGE STRATEGY:

{page_strategy_json}


PAGE BLUEPRINT:

{page_blueprint_json}


MESSAGE STRATEGY:

{message_strategy_json}


OFFER STRATEGY:

{offer_strategy_json}

"""


def generate_page_content_plan_handler(
    knowledge_id: int,
    brand_marketing_id: int,
    marketing_strategy_id: int,
    offer_strategy_id: int,
    message_strategy_id: int,
    page_strategy_id: int,
    page_blueprint_id: int,
):

    container = Container()

    knowledge_service = container.knowledge_service()
    brand_marketing_service = container.brand_marketing_service()
    marketing_strategy_service = container.marketing_strategy_service()
    page_strategy_service = container.page_strategy_service()
    page_blueprint_service = container.page_blueprint_service()
    message_strategy_service = container.message_strategy_service()
    offer_strategy_service = container.offer_strategy_service()

    page_content_plan_repository = container.page_content_plan_repository()
    page_content_plan_service = container.page_content_plan_service()

    ollama_service = container.ollama_service()


    page_blueprint = (
        page_blueprint_service.get_page_blueprint_by_id(
            id=page_blueprint_id
        )
    )


    page_strategy = (
        page_strategy_service.get_page_strategy_by_id(
            id=page_strategy_id
        )
    )


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


    offer_strategy = (
        offer_strategy_service.get_offer_strategy_by_id(
            id=offer_strategy_id
        )
    )


    brand_marketing = (
        brand_marketing_service.get_brand_marketing_by_id(
            id=brand_marketing_id
        )
    )


    marketing_strategy = (
        marketing_strategy_service.get_marketing_strategy_by_id(
            id=marketing_strategy_id
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

        brand_marketing_json=serialize(brand_marketing),

        marketing_strategy_json=serialize(marketing_strategy),

        page_strategy_json=serialize(page_strategy),

        page_blueprint_json=serialize(page_blueprint),

        message_strategy_json=serialize(message_strategy),

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


    page_content_plan_data = result.get("page_content_plan", {})


    entity = PageContentPlan(

        page_blueprint_id=page_blueprint_id,

        sections=page_content_plan_data.get("sections", []),

    )


    created = page_content_plan_repository.create(entity)


    return page_content_plan_service.get_page_content_plan_by_id(id=created.id)
