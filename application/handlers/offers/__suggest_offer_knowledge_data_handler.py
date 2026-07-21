import json
from di.container import Container
from application.mappers.offer_knowledge_mapper import OfferKnowledgeMapper
from domain.models.ollama.llm_ollama_message import LlmOllamaMessage
from domain.enums.ollama_message_role import OllamaMessageRole
from infrastructure.ai.prompts.constraints.uniqueness_prompt import build_uniqueness_constraint_prompt
from domain.enums.knowledge_insight_type import KnowledgeInsightType
from domain.models.knowledge.knowledge_insight import KnowledgeInsight
from domain.enums.content_status import ContentStatus


def get_system_prompt(knowledge_data: str):
    return f"""
You are an expert in product strategy, market research, and consumer psychology.
You specialize in deepening existing product/offer knowledge bases with additional,
non-obvious insights that help marketing and sales teams communicate value more effectively.

You think like an experienced product strategist and market analyst: you look for
angles, benefits, and differentiators that are not yet documented, without inventing
facts that are not grounded in the product data.

You base your conclusions on available data, clearly distinguish facts from
assumptions, and focus on practical business value.

Currently analyzed product knowledge:

```json
{knowledge_data}"""


FEATURES_AND_BENEFITS_PROMPT = """
Analyze the product knowledge and generate additional, realistic feature and benefit insights.

Return a JSON object with exactly these keys, each a list of strings:

{
    "feature": [],
    "functional_benefit": [],
    "emotional_benefit": []
}

Definitions:
- "feature": a concrete, factual capability or element the product/offer has.
- "functional_benefit": what the customer can practically do or achieve because of a feature.
- "emotional_benefit": how the customer feels as a result of using the product/offer.

Rules:
- Stay grounded in the product's actual purpose and existing knowledge.
- Do not invent features that are not plausible for this product.
- Do not repeat or lightly rephrase existing insights.
- Each item must add new, non-obvious value.
- Any of the three lists may be empty if no new meaningful insight exists — do not pad with filler.

Return only valid JSON in the structure above. No markdown, no comments.
"""


POSITIONING_PROMPT = """
Analyze the product knowledge and generate additional, realistic positioning insights.

Return a JSON object with exactly these keys, each a list of strings:

{
    "differentiator": [],
    "strength": [],
    "limitation": []
}

Definitions:
- "differentiator": what meaningfully sets this offer apart from typical alternatives.
- "strength": a clear advantage of the offer, grounded in its actual data.
- "limitation": an honest, realistic constraint or weakness of the offer.

Rules:
- Do not invent competitors or claims that cannot be inferred from the product data.
- Do not repeat or lightly rephrase existing insights.
- "limitation" must be realistic and fair, not exaggerated or invented for effect.
- Each item must add new, non-obvious value.
- Any of the three lists may be empty if no new meaningful insight exists — do not pad with filler.

Return only valid JSON in the structure above. No markdown, no comments.
"""


ADDITIONAL_INSIGHTS_PROMPT = """
Analyze the product knowledge and generate additional miscellaneous strategic insights
that do not fit cleanly into features, benefits, or positioning, but are still valuable
for marketing or sales.

Return a JSON object with exactly this key:

{
    "additional_insight": []
}

Rules:
- Focus on observations that could meaningfully change how this offer is marketed or sold.
- Do not repeat or lightly rephrase existing insights.
- Do not restate features, benefits, or positioning already covered elsewhere.
- The list may be empty if no new meaningful insight exists — do not pad with filler.

Return only valid JSON in the structure above. No markdown, no comments.
"""


# Grouped LLM calls: each entry maps a prompt to the KnowledgeInsightType(s) it produces.
SUGGESTION_GROUPS = [
    (
        FEATURES_AND_BENEFITS_PROMPT,
        {
            "feature": KnowledgeInsightType.FEATURE,
            "functional_benefit": KnowledgeInsightType.FUNCTIONAL_BENEFIT,
            "emotional_benefit": KnowledgeInsightType.EMOTIONAL_BENEFIT,
        },
    ),
    (
        POSITIONING_PROMPT,
        {
            "differentiator": KnowledgeInsightType.DIFFERENTIATOR,
            "strength": KnowledgeInsightType.STRENGTH,
            "limitation": KnowledgeInsightType.LIMITATION,
        },
    ),
    (
        ADDITIONAL_INSIGHTS_PROMPT,
        {
            "additional_insight": KnowledgeInsightType.ADDITIONAL_INSIGHT,
        },
    ),
]


def suggest_offer_knowledge_data_handler(knowledge_id: int):
    container = Container()
    offer_knowledge_repository = container.offer_knowledge_repository()
    knowledge_insights_repository = container.knowledge_insights_repository()
    offer_knowledge_assembler = container.offer_knowledge_assembler()
    ollama_service = container.ollama_service()

    offer_knowledge_db = offer_knowledge_repository.get_by_id(id=knowledge_id)

    if not offer_knowledge_db:
        raise ValueError(f"Offer knowledge {knowledge_id} not found")

    offer_knowledge_dto = OfferKnowledgeMapper.to_dto(item=offer_knowledge_db)
    offer_knowledge_assembled = offer_knowledge_assembler.assemble_dto(item=offer_knowledge_dto)

    knowledge_json = json.dumps(offer_knowledge_assembled.to_dict())

    generated_insights = []

    for prompt, type_mapping in SUGGESTION_GROUPS:
        existing_items = {
            field: [
                i.value
                for i in offer_knowledge_assembled.offer_insights
                if i.type == insight_type
            ]
            for field, insight_type in type_mapping.items()
        }

        messages = [
            LlmOllamaMessage(
                role=OllamaMessageRole.SYSTEM,
                content=get_system_prompt(knowledge_json),
            ),
            LlmOllamaMessage(
                role=OllamaMessageRole.USER,
                content=build_uniqueness_constraint_prompt(json.dumps(existing_items)),
            ),
            LlmOllamaMessage(
                role=OllamaMessageRole.USER,
                content=prompt,
            ),
        ]

        response = ollama_service.chat_llm(messages=messages)
        parsed = json.loads(response.content)

        for field, insight_type in type_mapping.items():
            for value in parsed.get(field, []):
                new_insight = KnowledgeInsight(
                    offer_id=offer_knowledge_assembled.offer_id,
                    knowledge_id=knowledge_id,
                    type=insight_type.value,
                    content_status=ContentStatus.SUGGESTED.value,
                    value=value,
                )
                generated_insights.append(new_insight)
                offer_knowledge_assembled.offer_insights.append(new_insight)

    knowledge_insights_repository.create_many(items=generated_insights)

    # --------------------------
    #  Return full offer knowledge data
    # --------------------------
    updated_offer_knowledge_db = offer_knowledge_repository.get_by_id(id=knowledge_id)
    updated_offer_knowledge_dto = OfferKnowledgeMapper.to_dto(item=updated_offer_knowledge_db)
    updated_offer_knowledge_assembled = offer_knowledge_assembler.assemble_dto(
        item=updated_offer_knowledge_dto
    )

    return updated_offer_knowledge_assembled
