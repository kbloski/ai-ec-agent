import json

from di.container import Container
from domain.models.ollama.llm_ollama_message import LlmOllamaMessage
from domain.enums.ollama_message_role import OllamaMessageRole
from domain.models.page_blueprint.page_blueprint import PageBlueprint


SYSTEM_PROMPT = """
You are an expert in:

- E-commerce Landing Page Architecture
- Conversion Rate Optimization
- Direct Response Marketing
- Product Page Psychology
- Customer Journey Design


Your task is to create a PAGE BLUEPRINT
for a sales-focused landing page of a physical product.


Page Blueprint is NOT final copy.

It defines:

- page structure,
- section order,
- purpose of each section,
- customer journey flow,
- content requirements needed later to generate copy.


Do NOT generate:

- headlines,
- subheadlines,
- body copy,
- CTA text,
- sales copy,
- HTML,
- CSS,
- UI components,
- visual design,
- images.



LANDING PAGE GOAL:

ATTENTION > PROBLEM AWARENESS > PRODUCT DESIRE > VALUE UNDERSTANDING > TRUST > PURCHASE DECISION



CONTEXT:

You mainly create blueprints for:

- e-commerce,
- physical products,
- low ticket products,
- direct response marketing,
- single product landing pages.



CONTEXT PRIORITY:

When information conflicts:

1. Follow Page Strategy.
2. Follow Offer Strategy.
3. Follow Message Strategy.
4. Use Knowledge Base as supporting context.

Do not create sections that conflict with the provided strategy.



AVAILABLE SECTION TYPES:


hero

Purpose:
First customer interaction.
Communicates the main product value.


problem

Purpose:
Shows the customer's problem, frustration, pain point, or unmet need.


solution

Purpose:
Positions the product as the solution to the customer's problem.


benefits

Purpose:
Shows customer outcomes, transformations, and product benefits.


features

Purpose:
Shows specific product characteristics and capabilities.


how_it_works

Purpose:
Explains how the product works.


social_proof

Purpose:
Builds trust through evidence and validation.


offer

Purpose:
Explains what the customer receives.


risk_reversal

Purpose:
Reduces purchase risk.


faq

Purpose:
Removes remaining questions and objections.


final_cta

Purpose:
Moves the customer toward purchase decision.



OPTIONAL SECTION TYPES:


product_showcase

Use when the product requires visual explanation.


comparison

Use when customers compare solutions or alternatives.


testimonials

Use when customer opinions strongly influence conversion.


before_after

Use when the product creates a visible transformation.


unique_mechanism

Use when explaining why the product works.


bonus_stack

Use when the offer contains additional value elements.


urgency

Use only when there is a real reason for immediate action.


pricing

Use when price or product variants influence the purchase decision.



SECTION TYPE RULES:

- Use only section types from the predefined list.
- Never create new section_type values.
- Never rename section types.
- Never combine multiple section types into one.
- Never remove required sections from Page Blueprint input.



SECTION SELECTION RULES:

Do not use every available section.

Choose only sections necessary for conversion.

For most e-commerce low ticket products, the common structure is:

hero
problem
solution
benefits
features
social_proof
offer
risk_reversal
faq
final_cta


Do not add:

- B2B case studies,
- unnecessary strategy sections,
- marketing analysis,
- final copy.



SECTION PRIORITY:

Use:

"required"
when the section is necessary for conversion.

Use:

"optional"
when the section can improve conversion but is not required.



SECTION CONTENT RULES:

The blueprint should describe:

- why the section exists,
- what customer state it addresses,
- what psychological role it plays,
- what information is required.

Do not describe:

- page layout,
- UI structure,
- components,
- visual implementation.

"required_content_elements" describe content requirements, not UI components.



SECTION COUNT:

- Generate only sections necessary for conversion.
- Avoid unnecessary sections.
- Prefer a clear conversion-focused structure.



OUTPUT JSON:

{
    "page_blueprint": {
        "page_type": "",
        "primary_conversion_goal": "",
        "sections": [
            {
                "order": 1,
                "section_type": "",
                "section_priority": "",
                "purpose": "",
                "customer_journey_stage": "",
                "conversion_role": "",
                "psychological_goal": "",
                "required_content_elements": [],
                "proof_elements": [],
                "objection_targets": [],
                "notes": ""
            }
        ]
    }
}



STRICT JSON RULES:
- Return only valid JSON.
- Root JSON must contain "page_blueprint".
- page_blueprint must contain "sections".
- sections must always be an array.
- Every section must be an object.
"""


USER_PROMPT_TEMPLATE = """
Generate Page Blueprint based on:


KNOWLEDGE BASE:
{knowledge_json}


PAGE STRATEGY:
{page_strategy_json}


MESSAGE STRATEGY:
{message_strategy_json}


BRAND STRATEGY:
{brand_strategy_json}


MARKETING STRATEGY:
{marketing_strategy_json}


OFFER STRATEGY:
{offer_strategy_json}
"""



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



def generate_page_blueprint_handler(
    page_strategy_id: int
):

    container = Container()


    page_strategy_service = (
        container.page_strategy_service()
    )

    message_strategy_service = (
        container.message_strategy_service()
    )

    knowledge_service = (
        container.knowledge_service()
    )

    brand_marketing_service = (
        container.brand_marketing_service()
    )

    marketing_strategy_service = (
        container.marketing_strategy_service()
    )

    offer_strategy_service = (
        container.offer_strategy_service()
    )


    page_blueprint_repository = (
        container.page_blueprint_repository()
    )

    page_blueprint_service = (
        container.page_blueprint_service()
    )

    ollama_service = (
        container.ollama_service()
    )



    page_strategy = (
        page_strategy_service
        .get_page_strategy_by_id(
            id=page_strategy_id
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


    brand_strategy = (
        brand_marketing_service
        .get_brand_marketing_by_id(
            id=marketing_strategy.brand_marketing_id
        )
    )


    knowledge = (
        knowledge_service
        .get_knowledge_details_by_id(
            knowledge_id=brand_strategy.knowledge_id
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

        knowledge_json=serialize(
            knowledge
        ),

        page_strategy_json=serialize(
            page_strategy
        ),

        message_strategy_json=serialize(
            message_strategy
        ),

        brand_strategy_json=serialize(
            brand_strategy
        ),

        marketing_strategy_json=serialize(
            marketing_strategy
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


        result = json.loads(
            content
        )


    except Exception as e:

        return {

            "error": "Invalid JSON response",

            "exception": str(e),

            "raw_response": response.content

        }



    page_blueprint_data = (
        result.get(
            "page_blueprint",
            {}
        )
    )



    if not page_blueprint_data:

        return {

            "error": "Missing page_blueprint",

            "raw_response": response.content

        }



    sections = (
        page_blueprint_data.get(
            "sections",
            []
        )
    )



    if not isinstance(
        sections,
        list
    ):

        return {

            "error": "Sections must be list",

            "raw_response": response.content

        }



    allowed_sections = {

        "hero",
        "problem",
        "solution",
        "benefits",
        "features",
        "how_it_works",
        "social_proof",
        "offer",
        "risk_reversal",
        "faq",
        "final_cta",
        "product_showcase",
        "comparison",
        "testimonials",
        "before_after",
        "unique_mechanism",
        "bonus_stack",
        "urgency",
        "pricing"

    }



    for section in sections:


        if (
            section.get("section_type")
            not in allowed_sections
        ):

            return {

                "error": "Invalid section_type",

                "section": section

            }



    entity = PageBlueprint(

        page_strategy_id=page_strategy_id,

        page_type=(
            page_blueprint_data.get(
                "page_type",
                "ecommerce_product"
            )
        ),

        primary_conversion_goal=(
            page_blueprint_data.get(
                "primary_conversion_goal",
                "purchase"
            )
        ),

        sections=sections

    )



    created = (
        page_blueprint_repository.create(
            entity
        )
    )



    return (
        page_blueprint_service
        .get_page_blueprint_by_id(
            id=created.id
        )
    )