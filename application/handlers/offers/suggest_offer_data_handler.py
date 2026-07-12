import json
from di.container import Container
from application.mappers.offer_mapper import OfferMapper
from domain.models.ollama.llm_ollama_message import LlmOllamaMessage
from domain.enums.ollama_message_role import OllamaMessageRole
from infrastructure.ai.prompts.constraints.uniqueness_prompt import build_uniqueness_constraint_prompt  
from domain.enums.offer_insight_type import OfferInsightType
from domain.models.offers.offer_insight import OfferInsight
from domain.enums.content_status import ContentStatus


def get_system_prompt(offer_data: str):
    SYSTEM_PROMPT = f"""
You are an expert in e-commerce strategy, product marketing, and consumer psychology.
You specialize in product analysis, customer behavior, buying motivations, and creating effective sales arguments.

You think like an experienced marketer and market analyst: you look for hidden customer needs, purchase drivers, problems, objections, and opportunities to increase product attractiveness.

You base your conclusions on available data, analyze products from the customer's perspective, and clearly distinguish facts from assumptions. Your goal is to provide practical business insights that can help improve product positioning, marketing communication, and sales performance.

Currently analyzed product:

```json
{offer_data}"""


PAIN_POINTS_PROMPT = """
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

Generate several realistic customer pain points.
"""


TARGET_AUDIENCE_PROMPT = """
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

Generate several additional customer segments.
"""



def suggets_offer_data_handler(offer_id : int):
    container = Container()
    offer_repository = container.offers_repository()
    offer_insights_repository = container.offer_insights_repository()
    offer_assembler = container.offer_assembler()
    ollama_service  = container.ollama_service()

    offer_db = offer_repository.get_by_id(id=offer_id)
    offer_dto = OfferMapper.to_dto(item=offer_db)
    offer_assembled = offer_assembler.assemble_dto(item=offer_dto)
    
    offer_pain_points = [p.to_dict() for p in offer_assembled.offer_insights if p.type == OfferInsightType.PAIN_POINTS]
    offer_target_audience = [p.to_dict() for p in offer_assembled.offer_insights if p.type == OfferInsightType.TARGET_AUDIENCE]

    generated_offer_insights = []

    # ---------------------------------------
    # PAIN POINTS
    # ---------------------------------------
    messages = [
        LlmOllamaMessage(
            role = OllamaMessageRole.SYSTEM,
            content = get_system_prompt(offer_assembled.to_dict())
        ),
        LlmOllamaMessage(
            role=OllamaMessageRole.USER,
            content=build_uniqueness_constraint_prompt( json.dumps(offer_pain_points))
        ),
        LlmOllamaMessage(
            role=OllamaMessageRole.USER,
            content=PAIN_POINTS_PROMPT
        )
    ]

    response_pain_points = ollama_service.chat_llm(messages=messages)
    new_pain_points_arr = json.loads(response_pain_points.content)
    for p in new_pain_points_arr:
        new_insights = OfferInsight(
            offer_id = offer_id,
            type = OfferInsightType.PAIN_POINTS.value,
            content_status = ContentStatus.SUGGESTED.value,
            value=p
        )
        generated_offer_insights.append(new_insights)
        offer_assembled.offer_insights.append(new_insights)


    # ---------------------------------------
    # Target audience
    # ---------------------------------------
    messages = [
        LlmOllamaMessage(
            role = OllamaMessageRole.SYSTEM,
            content = get_system_prompt(offer_assembled.to_dict())
        ),
        LlmOllamaMessage(
            role=OllamaMessageRole.USER,
            content=build_uniqueness_constraint_prompt( json.dumps(offer_target_audience))
        ),
        LlmOllamaMessage(
            role=OllamaMessageRole.USER,
            content=TARGET_AUDIENCE_PROMPT
        )
    ]

    response_target_audience = ollama_service.chat_llm(messages=messages)
    new_target_audience = json.loads(response_target_audience.content)
    for p in new_target_audience:
        new_insights =OfferInsight(
            offer_id = offer_id,
            type = OfferInsightType.TARGET_AUDIENCE.value,
            content_status = ContentStatus.SUGGESTED.value,
            value=p
        )
        generated_offer_insights.append(new_insights)
        offer_assembled.offer_insights.append(new_insights)

    # return generated_offer_insights
    offer_insights_repository.create_many(items=generated_offer_insights)

    # --------------------------
    #  Return full offer data
    # --------------------------
    updated_offer_db = offer_repository.get_by_id(id=offer_id)
    updated_offer_dto = OfferMapper.to_dto(item=updated_offer_db)
    updated_offer_assembled = offer_assembler.assemble_dto(item=updated_offer_dto)

    return updated_offer_assembled