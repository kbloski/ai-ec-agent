import json

from di.container import Container
from domain.models.ollama.llm_ollama_message import LlmOllamaMessage
from domain.enums.ollama_message_role import OllamaMessageRole
from domain.models.page_copy.page_copy import PageCopy


SYSTEM_PROMPT = """
You are an expert in:

- Conversion Copywriting
- Direct Response Marketing
- E-commerce Copywriting
- Landing Page Copywriting
- Customer Psychology
- Persuasive Writing
- Offer Communication
- Low Ticket Product Marketing


PAGE COPY is the final textual layer of a landing page.

Your task is to generate final customer-facing copy based on the provided marketing context.

You create:

- headline,
- subheadline,
- body_copy,
- bullet_points,
- content_blocks,
- CTA,
- supporting_text.


You do NOT create:

- strategy,
- analysis,
- explanations,
- recommendations,
- UI structure,
- design concepts.


GENERATION RULES:


1. PAGE CONTENT PLAN is the source of truth.

For every planned section:

- generate exactly one matching section,
- keep the same order,
- keep the same section_type,
- do not skip sections,
- do not add new sections.


2. Every section must:

- communicate product value,
- show customer transformation,
- remove objections,
- build trust,
- increase purchase desire,
- support conversion.


3. Copy rules:

- Write clear and persuasive customer-facing copy.
- Focus on benefits, outcomes, and customer motivation.
- Match the brand positioning.
- Use customer psychology principles.
- Make the copy specific to the product.

Do not invent facts.

Use only information available in the provided context.

Avoid generic marketing phrases.


Do not use:

- best product,
- #1,
- revolutionary,
- breakthrough,
- unique,
- amazing,
- incredible,
- game-changing,
- or similar unsupported claims.


Use specific benefits, mechanisms, proof points, and customer outcomes instead.



CONTENT_BLOCKS RULES:


content_blocks are optional internal elements inside a section.

They are NOT sections.

Never:

- create new sections from content_blocks,
- change the section order,
- create content_blocks when they are not needed,
- create new content_block types.


section_type defines what type of content_blocks can be used.


ALLOWED CONTENT_BLOCK MAPPING:


problem:

Use when the section presents multiple customer problems.

Format:

{
    "type": "problem_item",
    "title": "",
    "description": ""
}



benefits:

Use when the section presents multiple product benefits.

Format:

{
    "type": "benefit",
    "title": "",
    "description": ""
}



features:

Use when the section presents product features or specifications.

Format:

{
    "type": "feature",
    "title": "",
    "description": "",
    "specification": ""
}



offer:

Use when the section presents offer packages or included items.

Format:

{
    "type": "offer_card",
    "name": "",
    "price": "",
    "included_items": [],
    "cta": ""
}



faq:

Use when the section contains multiple customer questions and answers.

Format:

{
    "type": "faq_item",
    "question": "",
    "answer": ""
}



comparison:

Use when the section compares the product with alternatives.

Format:

{
    "type": "comparison_row",
    "criterion": "",
    "product_value": "",
    "alternative_value": ""
}



CONTENT_BLOCK RULES:

- content_blocks expand an existing section.
- content_blocks never replace sections.
- Every content_block must match the section_type.
- Do not create content_blocks for sections that do not require structured elements.



SECTION TYPE MUST BE ONE OF:

hero
problem
solution
benefits
features
how_it_works
social_proof
testimonials
case_studies
comparison
offer
pricing
risk_reversal
objection_handling
faq
final_cta



OUTPUT FORMAT:

Return exactly this JSON structure:


{
    "page_copy": {
        "sections": [
            {
                "order": 1,
                "section_type": "",
                "headline": "",
                "subheadline": "",
                "body_copy": "",
                "bullet_points": [],
                "content_blocks": [],
                "cta": "",
                "supporting_text": ""
            }
        ]
    }
}



STRICT JSON RULES:
- Return only valid JSON.
"""


USER_PROMPT_TEMPLATE = """
Generate Page Copy based on the following marketing context:

KNOWLEDGE BASE:
{knowledge_json}


BRAND MARKETING STRATEGY:
{brand_marketing_json}


MARKETING STRATEGY:
{marketing_strategy_json}


PAGE BLUEPRINT:
{page_blueprint_json}


PAGE CONTENT PLAN:
{page_content_plan_json}


PAGE STRATEGY:
{page_strategy_json}


MESSAGE STRATEGY:
{message_strategy_json}


OFFER STRATEGY:
{offer_strategy_json}
"""



def normalize_json(content: str):

    replacements = {
        "‚": "'",
        "’": "'",
    }

    for old, new in replacements.items():
        content = content.replace(old, new)

    return content.strip()



def extract_json(content: str):

    content = content.strip()

    if "```" in content:

        content = (
            content
            .replace("```json", "")
            .replace("```", "")
            .strip()
        )


    start = content.find("{")
    end = content.rfind("}")


    if start == -1 or end == -1:

        raise ValueError(
            "JSON object not found"
        )


    return content[start:end + 1]



def generate_page_copy_handler(
    page_content_plan_id: int
):

    container = Container()


    page_content_plan_service = container.page_content_plan_service()
    page_strategy_service = container.page_strategy_service()
    message_strategy_service = container.message_strategy_service()
    offer_strategy_service = container.offer_strategy_service()

    knowledge_service = container.knowledge_service()
    brand_marketing_service = container.brand_marketing_service()
    marketing_strategy_service = container.marketing_strategy_service()

    page_blueprint_service = container.page_blueprint_service()

    page_copy_repository = container.page_copy_repository()
    page_copy_service = container.page_copy_service()

    ollama_service = container.ollama_service()



    page_content_plan = (
        page_content_plan_service
        .get_page_content_plan_by_id(
            id=page_content_plan_id
        )
    )


    page_blueprint = (
        page_blueprint_service
        .get_page_blueprint_by_id(
            id=page_content_plan.page_blueprint_id
        )
    )


    page_strategy = (
        page_strategy_service
        .get_page_strategy_by_id(
            id=page_blueprint.page_strategy_id
        )
    )


    message_strategy = (
        message_strategy_service
        .get_message_strategy_by_id(
            id=page_strategy.message_strategy_id
        )
    )


    offer_strategy = (
        offer_strategy_service
        .get_offer_strategy_by_id(
            id=message_strategy.offer_strategy_id
        )
    )


    marketing_strategy = (
        marketing_strategy_service
        .get_marketing_strategy_by_id(
            id=offer_strategy.marketing_strategy_id
        )
    )


    brand_marketing = (
        brand_marketing_service
        .get_brand_marketing_by_id(
            id=marketing_strategy.brand_marketing_id
        )
    )


    knowledge = (
        knowledge_service
        .get_knowledge_details_by_id(
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

        brand_marketing_json=serialize(
            brand_marketing
        ),

        marketing_strategy_json=serialize(
            marketing_strategy
        ),

        page_blueprint_json=serialize(
            page_blueprint
        ),

        page_content_plan_json=serialize(
            page_content_plan
        ),

        page_strategy_json=serialize(
            page_strategy
        ),

        message_strategy_json=serialize(
            message_strategy
        ),

        offer_strategy_json=serialize(
            offer_strategy
        )

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

        content = extract_json(
            response.content
        )


        content = normalize_json(
            content
        )


        result = json.loads(
            content
        )


    except Exception as e:

        return {

            "error": "Invalid JSON response",

            "exception": str(e),

            "raw_response": response.content

        }



    if "page_copy" not in result:

        return {

            "error": "Missing page_copy",

            "raw_response": response.content

        }


    page_copy_data = result.get("page_copy", {})


    entity = PageCopy(

        page_content_plan_id=page_content_plan_id,

        sections=page_copy_data.get("sections", []),

    )


    created = page_copy_repository.create(entity)


    return page_copy_service.get_page_copy_by_id(id=created.id)