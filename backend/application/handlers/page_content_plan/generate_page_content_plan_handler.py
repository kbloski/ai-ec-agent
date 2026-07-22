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


Page Blueprint defines the page architecture.

It specifies:
- which sections exist,
- their order,
- the purpose of each section,
- required elements,
- proof elements,
- objection targets.


Page Content Plan does NOT modify the page architecture.

Instead, it expands each Page Blueprint section into a content planning document that defines:

- what each section should communicate,
- what information should be included,
- what arguments should be presented,
- what supporting evidence should be included,
- what objections should be addressed,
- what information the final copy should contain.


Page Content Plan answers:

"What content and arguments should each page section contain?"


IMPORTANT

Page Content Plan is NOT final copy.

Do not generate:

- headlines,
- subheadlines,
- slogans,
- CTA copy,
- advertising copy,
- customer-facing sentences,
- UI components,
- layouts,
- HTML,
- CSS.


Generate only:

- communication direction,
- content requirements,
- key arguments,
- psychological purpose,
- conversion logic.


PRIORITY RULES

When information conflicts:

1. Follow Page Blueprint.
2. Follow Page Strategy.
3. Follow Message Strategy.
4. Follow Offer Strategy.
5. Follow Marketing Strategy.
6. Follow Brand Marketing.
7. Use Knowledge Base as supporting context.


FIELD DEFINITIONS

content_goal
Describe the purpose of the content within this section.

customer_question
The main question the customer expects this section to answer.

customer_state
The customer's psychological state before reading the section.

main_message_direction
The strategic communication direction for the section.

content_elements
Describe the information that should appear in the section.

key_arguments
The strongest arguments supporting the section objective.

emotional_points
Emotional motivations the section should reinforce.

rational_points
Logical reasons supporting the purchase decision.

proof_needed
Describe the specific supporting evidence that should appear in the section.

Examples:
- customer testimonials
- review screenshots
- statistics
- certifications
- guarantees
- expert recommendations
- before/after examples
- product demonstrations

Use the corresponding Page Blueprint "proof_elements" as input and expand them into practical content requirements.

objections_addressed
Describe the specific customer objections that the section should resolve.

Use the corresponding Page Blueprint "objection_targets" as input and explain how the content should address them.

cta_role
Describe the strategic role of the CTA within the section.

visual_support_needed
Describe which visual assets would strengthen the communication.

Examples:
- lifestyle photography
- product close-ups
- comparison graphics
- customer review screenshots
- icons
- diagrams

notes
Additional guidance for the future copywriting stage.


RULES

- Every generated section must correspond exactly to one Page Blueprint section.
- Preserve the same section order.
- Do not add sections.
- Do not remove sections.
- Do not rename section types.
- Do not merge sections.
- Do not split sections.
- Expand the Page Blueprint instead of repeating it.
- Every field must exist.
- Arrays must always be arrays.
- Do not use null values.
- Return only valid JSON.


VALIDATION

If a Page Blueprint section contains "proof_elements",
the generated section must populate "proof_needed".

If a Page Blueprint section contains "objection_targets",
the generated section must populate "objections_addressed".

Do not leave these arrays empty unless the corresponding Page Blueprint arrays are also empty.


JSON FORMAT

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


STRICT JSON RULES

- Return only valid JSON.
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
