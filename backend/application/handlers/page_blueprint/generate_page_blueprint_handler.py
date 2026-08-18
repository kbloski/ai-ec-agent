import json
from typing import Optional

from di.container import Container
from domain.enums.llm_message_role import LlmMessageRole
from domain.enums.page_section_category import PageSectionCategory
from domain.models.llm.llm_message import LlmMessage
from domain.models.page_blueprint.page_blueprint import PageBlueprint


ALLOWED_SECTION_PRIORITIES = {"required", "optional"}
ALLOWED_CUSTOMER_JOURNEY_STAGES = {
    "Attention",
    "Problem Awareness",
    "Product Desire",
    "Value Understanding",
    "Trust",
    "Purchase Decision",
}
REQUIRED_SECTION_KEYS = {
    "order",
    "section_type",
    "section_priority",
    "purpose",
    "customer_journey_stage",
    "conversion_role",
    "psychological_goal",
    "required_content_elements",
    "proof_elements",
    "objection_targets",
}
ARRAY_SECTION_KEYS = {
    "required_content_elements",
    "proof_elements",
    "objection_targets",
}


def generate_page_blueprint_handler(page_strategy_id: int):
    container = Container()

    page_strategy_service = container.page_strategy_service()
    message_strategy_service = container.message_strategy_service()
    knowledge_service = container.knowledge_service()
    brand_marketing_service = container.brand_marketing_service()
    marketing_strategy_service = container.marketing_strategy_service()
    offer_strategy_service = container.offer_strategy_service()
    page_sections_service = container.page_sections_service()
    page_blueprint_repository = container.page_blueprint_repository()
    page_blueprint_service = container.page_blueprint_service()
    ai_service = container.ai_service()

    page_strategy = page_strategy_service.get_page_strategy_by_id(
        id=page_strategy_id
    )

    message_strategy = message_strategy_service.get_message_strategy_by_id(
        id=page_strategy.message_strategy_id
    )

    offer_strategy = offer_strategy_service.get_offer_strategy_by_id(
        id=message_strategy.offer_strategy_id
    )

    marketing_strategy = marketing_strategy_service.get_marketing_strategy_by_id(
        id=offer_strategy.marketing_strategy_id
    )

    brand_strategy = brand_marketing_service.get_brand_marketing_by_id(
        id=marketing_strategy.brand_marketing_id
    )

    user_prompt = get_data_prompt(
        knowledge_context=knowledge_service.build_llm_context(
            knowledge_id=brand_strategy.knowledge_id
        ),
        brand_strategy_context=brand_marketing_service.build_llm_context(
            brand_marketing_id=marketing_strategy.brand_marketing_id
        ),
        marketing_strategy_context=marketing_strategy_service.build_llm_context(
            marketing_strategy_id=offer_strategy.marketing_strategy_id
        ),
        offer_strategy_context=offer_strategy_service.build_llm_context(
            offer_strategy_id=message_strategy.offer_strategy_id
        ),
        message_strategy_context=message_strategy_service.build_llm_context(
            message_strategy_id=page_strategy.message_strategy_id
        ),
        page_strategy_context=page_strategy_service.build_llm_context(
            page_strategy_id=page_strategy_id
        ),
    )

    response = ai_service.chat_llm(
        messages=[
            LlmMessage(
                role=LlmMessageRole.SYSTEM,
                content=get_system_prompt(
                    section_types_prompt=build_blueprint_taxonomy_prompt(
                        page_sections_service.get_all()
                    )
                ),
            ),
            LlmMessage(
                role=LlmMessageRole.USER,
                content=user_prompt,
            ),
            LlmMessage(
                role=LlmMessageRole.SYSTEM,
                content=(
                    "Generate the Page Blueprint now from the provided data. "
                    "Return only valid JSON using the specified structure. "
                    "Do not invent evidence, claims, objections, urgency, or scarcity."
                ),
            ),
        ]
    )

    try:
        result = parse_llm_json(response.content)
    except Exception as e:
        return {
            "error": "Invalid JSON response",
            "exception": str(e),
            "raw_response": response.content,
        }

    page_blueprint_data = result.get("page_blueprint", {})

    if not page_blueprint_data:
        return {
            "error": "Missing page_blueprint",
            "raw_response": response.content,
        }

    sections = page_blueprint_data.get("sections", [])

    if not isinstance(sections, list):
        return {
            "error": "Sections must be list",
            "raw_response": response.content,
        }

    allowed_sections = set(page_sections_service.get_allowed_ids())

    validation_error = validate_sections(
        sections=sections,
        allowed_sections=allowed_sections,
    )

    if validation_error:
        return {
            "error": "Invalid page blueprint",
            "details": validation_error,
            "raw_response": response.content,
        }

    entity = PageBlueprint(
        page_strategy_id=page_strategy_id,
        page_type=page_blueprint_data.get(
            "page_type",
            "ecommerce_product",
        ),
        primary_conversion_goal=page_blueprint_data.get(
            "primary_conversion_goal",
            "purchase",
        ),
        sections=sections,
    )

    created = page_blueprint_repository.create(entity)

    return page_blueprint_service.get_page_blueprint_by_id(
        id=created.id
    )


def parse_llm_json(raw_content: str) -> dict:
    if not isinstance(raw_content, str) or not raw_content.strip():
        raise ValueError("LLM returned empty response")

    content = raw_content.strip()

    if content.startswith("```"):
        lines = content.splitlines()

        if lines and lines[0].strip().startswith("```"):
            lines = lines[1:]

        if lines and lines[-1].strip() == "```":
            lines = lines[:-1]

        content = "\n".join(lines).strip()

    result = json.loads(content)

    if not isinstance(result, dict):
        raise ValueError("Root JSON value must be an object")

    return result


def validate_sections(
    sections: list,
    allowed_sections: set[str],
) -> Optional[str]:
    expected_orders = list(range(1, len(sections) + 1))
    actual_orders = []

    for index, section in enumerate(sections, start=1):
        if not isinstance(section, dict):
            return f"Section at index {index - 1} must be an object"

        missing_keys = REQUIRED_SECTION_KEYS - section.keys()
        if missing_keys:
            return (
                f"Section {index} is missing required keys: "
                f"{', '.join(sorted(missing_keys))}"
            )

        section_type = section.get("section_type")
        if section_type not in allowed_sections:
            return f"Section {index} has invalid section_type: {section_type}"

        section_priority = section.get("section_priority")
        if section_priority not in ALLOWED_SECTION_PRIORITIES:
            return (
                f"Section {index} has invalid section_priority: "
                f"{section_priority}"
            )

        journey_stage = section.get("customer_journey_stage")
        if journey_stage not in ALLOWED_CUSTOMER_JOURNEY_STAGES:
            return (
                f"Section {index} has invalid customer_journey_stage: "
                f"{journey_stage}"
            )

        order = section.get("order")
        if not isinstance(order, int) or isinstance(order, bool):
            return f"Section {index} order must be an integer"

        actual_orders.append(order)

        for key in ARRAY_SECTION_KEYS:
            if not isinstance(section.get(key), list):
                return f"Section {index} field '{key}' must be an array"

        for key in (
            "section_type",
            "section_priority",
            "purpose",
            "customer_journey_stage",
            "conversion_role",
            "psychological_goal",
        ):
            value = section.get(key)
            if not isinstance(value, str) or not value.strip():
                return f"Section {index} field '{key}' must be a non-empty string"

    if actual_orders != expected_orders:
        return (
            "Section order must be sequential and start at 1. "
            f"Expected {expected_orders}, got {actual_orders}"
        )

    return None


def build_blueprint_taxonomy_prompt(sections: list[dict]) -> str:
    core_sections = [
        section
        for section in sections
        if section["category"] == PageSectionCategory.CORE.value
    ]
    conditional_sections = [
        section
        for section in sections
        if section["category"] == PageSectionCategory.CONDITIONAL.value
    ]

    core_block = "\n\n\n".join(
        f"{section['id']}\n\nPurpose:\n{section['description']}"
        for section in core_sections
    )

    conditional_block = "\n\n\n".join(
        f"{section['id']}\n\nPurpose:\n{section['description']}"
        for section in conditional_sections
    )

    return (
        f"CORE SECTION TYPES:\n\n\n{core_block}"
        f"\n\n\n\nCONDITIONAL SECTION TYPES:\n\n\n{conditional_block}"
    )


def get_system_prompt(section_types_prompt: str) -> str:
    return """
You are an expert in:

- E-commerce Landing Page Architecture
- Conversion Rate Optimization
- Direct Response Marketing
- Product Page Psychology
- Customer Journey Design
- Consumer Psychology


Your task is to create a PAGE BLUEPRINT
for a sales-focused landing page of a physical product.


Page Blueprint is NOT final copy.

It defines:

- page structure,
- section order,
- purpose of each section,
- customer journey flow,
- psychological role of each section,
- content requirements needed later to generate copy,
- trust-building requirements,
- objection removal strategy.


Do NOT generate:

- headlines,
- subheadlines,
- body copy,
- CTA text,
- sales copy,
- advertising copy,
- HTML,
- CSS,
- UI components,
- visual design,
- images.


LANDING PAGE CUSTOMER JOURNEY:

Use only these exact customer_journey_stage values:

- Attention
- Problem Awareness
- Product Desire
- Value Understanding
- Trust
- Purchase Decision

The page should generally progress toward purchase, but not every stage
must have a dedicated section and multiple sections may belong to the same stage.


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
2. Follow explicit customer psychology and objections from the provided context.
3. Follow Offer Strategy.
4. Follow Message Strategy.
5. Follow Marketing Strategy.
6. Use Brand Strategy and Knowledge Base as supporting context.

Do not create sections, claims, proof, objections, offers, guarantees,
or strategies that conflict with the provided context.


""" + section_types_prompt + """


SECTION TAXONOMY SEMANTICS:

CORE means the section type is a strong general candidate for a sales page.
CORE does NOT mean the section is automatically required in this blueprint.

CONDITIONAL means the section should be selected only when the provided
product, customer, offer, objections, or page strategy creates a clear need for it.

Taxonomy category and section_priority are different concepts.


SECTION TYPE RULES:

- Use only section types from the predefined list.
- Never create new section_type values.
- Never rename section types.
- Never combine multiple section types into one.
- If the provided Page Strategy explicitly requires a section, include it.
- Every selected section must have a distinct and clear conversion purpose.


SECTION SELECTION RULES:

Build the page structure from the provided strategy and customer psychology.

Do NOT start from a predefined landing-page template.
Do NOT automatically include all CORE section types.
Do NOT include a section merely because it is common on e-commerce pages.

Evaluate every possible section independently.
Select it only when it has a clear strategic role for this specific product,
customer, offer, objections, and conversion goal.

CONDITIONAL sections should be included only when the context creates
a clear strategic need for them.

Avoid redundant sections whose conversion purpose substantially overlaps
with another selected section.

Prefer the smallest set of sections that creates a complete and persuasive
customer journey.

The final sequence must create the clearest possible progression toward
the primary conversion goal.


SECTION PRIORITY:

Use:

"required"

only when this specific blueprint needs the section to execute the provided
strategy or when removing it would create a meaningful conversion gap.

Use:

"optional"

when the section can improve this specific blueprint but can be removed
without breaking the core conversion strategy.

Do not derive section_priority mechanically from CORE or CONDITIONAL taxonomy.


SECTION CONTENT RULES:

The blueprint should describe:

- why the section exists,
- what customer state it addresses,
- what psychological role it plays,
- what information is required,
- what credible trust elements are available,
- what real objections it should remove when applicable.

required_content_elements must describe information or assets needed by the
section without inventing unsupported factual claims.

Do not describe:

- page layout,
- UI structure,
- components,
- visual implementation,
- final copy.


PROOF ELEMENTS RULES:

proof_elements describe evidence that is actually supported by the provided
context and can credibly be used on the page.

Never invent, assume, or fabricate:

- statistics,
- customer counts,
- testimonials,
- customer reviews,
- user-generated content,
- before/after results,
- certifications,
- awards,
- expert endorsements,
- scientific or clinical validation,
- guarantees,
- return policies,
- press mentions,
- popularity claims,
- product performance claims,
- scarcity,
- limited availability,
- limited-time offers.

A proof element may be included only when the provided context explicitly
supports that evidence or clearly states that the brand has it available.

If no credible proof element is supported for a section, return:

"proof_elements": []

Do not manufacture proof simply because evidence would theoretically
improve conversion.

proof_elements are an inventory of usable evidence, not a wishlist of
future evidence the brand should create.


OBJECTION TARGET RULES:

objection_targets describe real purchase barriers, doubts, or questions
that are supported by the provided context.

Assign objection_targets only when the section has a clear role in resolving
a real customer objection.

Do not invent objections merely to populate the field.
Do not reinterpret a general customer pain point as a purchase objection
unless the context supports that interpretation.

The same objection may appear in multiple sections only when each section
addresses it in a meaningfully different way.

If a section does not directly address a supported objection, return:

"objection_targets": []


URGENCY AND SCARCITY RULES:

Never create urgency or scarcity unless the provided context explicitly
supports a real reason for immediate action.

Do not invent:

- countdowns,
- deadlines,
- limited editions,
- limited stock,
- expiring prices,
- temporary bonuses,
- limited-time discounts.

If urgency or scarcity is not supported by the input, use neutral conversion
language focused on clarity, value, confidence, and decision friction.


EVIDENCE AND CLAIM SAFETY:

Never convert strategic ideas into factual claims.

A desired marketing angle is not evidence.
A customer pain point is not proof of product effectiveness.
A hypothetical proof idea is not an available proof asset.

Do not infer product effectiveness, scientific validity, health outcomes,
customer satisfaction rates, guarantees, scarcity, popularity, or expert
endorsement unless explicitly supported by the provided context.

For wellness, self-reflection, emotional wellbeing, health-adjacent,
or similar products, do not imply clinical, therapeutic, psychological,
or medical effectiveness unless explicitly supported by appropriate evidence
in the provided context.


SECTION COUNT:

- Generate only sections necessary for conversion.
- Avoid unnecessary sections.
- Avoid template-like section selection.
- Prefer a clear, logical customer journey.
- Every selected section must move the customer closer to purchase or remove
  a meaningful barrier to purchase.


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
                "objection_targets": []
            }
        ]
    }
}


FINAL VALIDATION BEFORE OUTPUT:

Before returning JSON verify:

- Root JSON contains "page_blueprint".
- page_blueprint contains "sections".
- sections is always an array.
- Every section is an object.
- Every section contains all required keys from the output structure.
- section_type values come only from the predefined taxonomy.
- section_priority is exactly "required" or "optional".
- customer_journey_stage uses only an allowed stage value.
- Section order starts at 1 and is sequential.
- proof_elements contains only evidence supported by the provided context.
- objection_targets contains only objections supported by the provided context.
- Empty proof_elements and objection_targets arrays are allowed.
- No unsupported urgency, scarcity, statistics, testimonials, guarantees,
  certifications, endorsements, or health claims are introduced.
- Section order follows customer journey logic.
- No final copy is generated.
- No explanations are added.


STRICT JSON RULES:

- Return only valid JSON.
- Do not use markdown.
- Do not add comments.
- Do not add explanations.
- Do not add text before JSON.
- Do not add text after JSON.
- Keep all JSON keys unchanged.
- Do not use null values.
- Arrays must always be arrays.
"""


def get_data_prompt(
    knowledge_context: str,
    brand_strategy_context: str,
    marketing_strategy_context: str,
    offer_strategy_context: str,
    message_strategy_context: str,
    page_strategy_context: str,
) -> str:
    return f"""
KNOWLEDGE:
{knowledge_context}


BRAND STRATEGY:
{brand_strategy_context}


MARKETING STRATEGY:
{marketing_strategy_context}


OFFER STRATEGY:
{offer_strategy_context}


MESSAGE STRATEGY:
{message_strategy_context}


PAGE STRATEGY:
{page_strategy_context}
"""