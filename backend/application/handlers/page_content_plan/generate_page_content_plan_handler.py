import json

from di.container import Container
from domain.models.ollama.llm_ollama_message import LlmOllamaMessage
from domain.enums.ollama_message_role import OllamaMessageRole
from domain.models.page_content_plan.page_content_plan import PageContentPlan

SYSTEM_PROMPT = """
You are an expert in:

- Landing Page Content Architecture
- Conversion Rate Optimization
- Direct Response Marketing
- Customer Psychology
- Marketing Content Planning


Your task is to create a PAGE CONTENT PLAN
based on the provided marketing context.


Page Content Plan defines:

- what each landing page section should communicate,
- what information should be included,
- what arguments should be used,
- what elements support conversion.


Page Content Plan answers:

"What content and arguments should each page section contain?"


IMPORTANT:

Page Content Plan is NOT final copy.

Do not generate:

- headlines,
- slogans,
- CTA text,
- advertising copy,
- final customer-facing sentences,
- UI components.


Generate only:

- communication direction,
- content requirements,
- key arguments,
- psychological purpose,
- conversion logic.



PRIORITY RULES:

When information conflicts:

1. Follow Page Blueprint.
2. Follow Page Strategy.
3. Follow Message Strategy.
4. Follow Offer Strategy.
5. Use Knowledge Base as supporting context.



RULES:

- Every section must match a section from Page Blueprint.
- Do not add new sections.
- Do not remove sections.
- Do not rename section types.
- Do not change section order.
- Do not merge or split sections.
- All fields must exist.
- Return only valid JSON.



JSON FORMAT:

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
                "content_elements": [],
                "key_arguments": [],
                "emotional_points": [],
                "rational_points": [],
                "proof_needed": [],
                "objections_addressed": [],
                "cta_role": "",
                "visual_support_needed": [],
                "notes": ""
            }
        ]
    }
}
"""


USER_PROMPT_TEMPLATE = """
Generate Page Content Plan based on:


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
    page_blueprint_id: int
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
            id=page_blueprint.page_strategy_id
        )
    )


    message_strategy = (
        message_strategy_service.get_message_strategy_by_id(
            id=page_strategy.message_strategy_id
        )
    )


    offer_strategy = (
        offer_strategy_service.get_offer_strategy_by_id(
            id=message_strategy.offer_strategy_id
        )
    )


    marketing_strategy = (
        marketing_strategy_service.get_marketing_strategy_by_id(
            id=offer_strategy.marketing_strategy_id
        )
    )


    brand_marketing = (
        brand_marketing_service.get_brand_marketing_by_id(
            id=marketing_strategy.brand_marketing_id
        )
    )


    knowledge = (
        knowledge_service.get_knowledge_details_by_id(
            knowledge_id=brand_marketing.knowledge_id
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
