import json
from typing import List
from di.container import Container
from application.mappers.offer_mapper import OfferMapper
from domain.models.llm.llm_message import LlmMessage
from domain.enums.llm_message_role import LlmMessageRole
from infrastructure.ai.prompts.uniqueness import build_uniqueness_prompt
from domain.enums.offer_insight_type import OfferInsightType
from domain.models.offers.offer_insight import OfferInsight
from domain.enums.fact_status import FactStatus



def generate_offer_insights_handler(offer_id: int, types: List[OfferInsightType]):
    container = Container()
    offer_repository = container.offers_repository()
    offer_insights_repository = container.offer_insights_repository()
    offer_assembler = container.offer_assembler()
    ai_service  = container.ai_service()

    offer_db = offer_repository.get_by_id(id=offer_id)
    offer_dto = OfferMapper.to_dto(item=offer_db)
    offer_assembled = offer_assembler.assemble_dto(item=offer_dto)

    generated_offer_insights = []

    for insight_type, prompt in INSIGHT_GENERATORS.items():
        if insight_type not in types:
            continue

        existing_insights = [
            p.to_dict() 
            for p in offer_assembled.offer_insights 
            if p.type == insight_type.value
        ]

        messages = [
            LlmMessage(
                role=LlmMessageRole.SYSTEM,
                content=get_system_prompt(json.dumps(offer_dto.to_content_dict()))
            ),
            LlmMessage(
                role=LlmMessageRole.USER,
                content=build_uniqueness_prompt(json.dumps(existing_insights))
            ),
            LlmMessage(
                role=LlmMessageRole.USER,
                content=prompt
            )
        ]

        response = ai_service.chat_llm(messages=messages)
        new_values = json.loads(response.content)
        for value in new_values:
            new_insight = OfferInsight(
                offer_id=offer_id,
                type=insight_type.value,
                fact_status=FactStatus.UNVERIFIED.value,
                value=value
            )
            generated_offer_insights.append(new_insight)
            offer_assembled.offer_insights.append(new_insight)

    if generated_offer_insights:
        offer_insights_repository.create_many(items=generated_offer_insights)

    # --------------------------
    #  Return full offer data
    # --------------------------
    updated_offer_db = offer_repository.get_by_id(id=offer_id)
    updated_offer_dto = OfferMapper.to_dto(item=updated_offer_db)
    updated_offer_assembled = offer_assembler.assemble_dto(item=updated_offer_dto)

    return updated_offer_assembled



def get_system_prompt(offer_data: str) -> str:
    return f"""
You are an expert in e-commerce strategy, product marketing, and consumer behavior.

Analyze the provided offer from the customer's perspective and generate practical marketing insights.

Rules:
- Use the provided offer data as the source of truth.
- You may make reasonable marketing inferences, but do not present them as verified facts.
- Do not invent product features, capabilities, results, prices, guarantees, or proof.
- Stay close to the product's actual purpose and positioning.
- Prefer specific, realistic insights over broad or generic ideas.
- Avoid duplicates and near-duplicates.

OFFER DATA:

{offer_data}
"""


def get_pain_points_prompt() -> str:
    return """
Analyze the product and identify realistic customer pain points that this product solves.

First, understand the product:
- what task it helps customers accomplish,
- what inconveniences it removes,
- what difficulties it reduces,
- what existing methods or tools it can improve.

Generate pain points based on real-life situations where a customer would need this product.

Rules:
- Stay within the product's actual purpose and capabilities.
- Do not invent completely new markets or unrelated use cases.
- Do not assume professional use if the product does not clearly support it.
- Do not create problems that are not directly related to the product.
- Do not describe product features, advantages, or marketing benefits.
- Describe the customer's situation before purchasing the product.
- Focus on frustration, difficulties, wasted time, effort, inconveniences, or limitations.

Treat existing pain points as context. Expand and complement them, but do not copy them blindly.

Return only valid JSON containing a list of strings.

Correct output example:
[ "string", "string" ]

Generate several realistic customer pain points.
"""


def get_target_audience_prompt() -> str:
    return """
Analyze the product and expand the existing target audience with additional realistic customer segments.

Find people who could naturally buy this product because they have a similar need or problem.

Base the analysis on:
- the current target audience,
- the product's purpose,
- product usage situations,
- customer problems.

Rules:
- Stay within the product's current positioning.
- Do not search for completely new markets.
- Do not create unlikely professional groups if the product does not fit their needs.
- Do not use broad groups such as "everyone", "people", or "customers".
- Each audience group must have a specific reason to buy this product.
- Focus on practical customer segments useful for marketing communication.
- Do not repeat existing audience groups.

Return only valid JSON containing a list of strings.

Correct output example:
[ "string", "string" ]

Generate several additional customer segments.
"""


INSIGHT_GENERATORS = {
    OfferInsightType.PAIN_POINTS: get_pain_points_prompt(),
    OfferInsightType.TARGET_AUDIENCE: get_target_audience_prompt(),
}
