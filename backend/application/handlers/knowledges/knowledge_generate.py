# ----------------------------
# Prepare dto result
# ----------------------------
import json

from application.mappers.knowledge_mapper import KnowledgeMapper
from application.mappers.knowledge_insight_mapper import KnowledgeInsightMapper
from application.dtos.offers.offer_dto import OfferDto

from di.container import Container
from domain.models.llm.llm_message import LlmMessage
from domain.enums.llm_message_role import LlmMessageRole

from domain.models.knowledge.knowledge import Knowledge
from domain.models.knowledge.knowledge_insight import KnowledgeInsight

from domain.enums.knowledge_insight_type import KnowledgeInsightType
from domain.enums.fact_status import FactStatus

from infrastructure.database.db import SessionLocal



# =====================================================
# INSIGHT TYPE MAPPING
# =====================================================

INSIGHT_MAPPING = {
    "problem_solved": KnowledgeInsightType.PROBLEM_SOLVED,
    "solution":KnowledgeInsightType.SOLUTION,
    "transformation":KnowledgeInsightType.TRANSFORMATION,
    "offer_components":KnowledgeInsightType.OFFER_COMPONENT,
    "features":KnowledgeInsightType.FEATURE,
    "functional_benefits":KnowledgeInsightType.FUNCTIONAL_BENEFIT,
    "emotional_benefits":KnowledgeInsightType.EMOTIONAL_BENEFIT,
    "differentiators":KnowledgeInsightType.DIFFERENTIATOR,
    "strengths":KnowledgeInsightType.STRENGTH,
    "limitations":KnowledgeInsightType.LIMITATION,
    "additional_insights":KnowledgeInsightType.ADDITIONAL_INSIGHT,
}



# =====================================================
# MAIN HANDLER
# =====================================================

def knowledge_generate_handler(offer_id: int):

    container = Container()

    offer_service = container.offer_service()
    ai_service = container.ai_service()


    # ----------------------------
    # LOAD OFFER
    # ----------------------------
    offer_context = offer_service.build_llm_context(offer_id)
    

    # ----------------------------
    # GENERATE KNOWLEDGE
    # ----------------------------

    chat = [
        LlmMessage(
            role=LlmMessageRole.SYSTEM,
            content=get_system_prompt()
        ),
        LlmMessage(
            role=LlmMessageRole.USER,
            content=get_data_prompt(offer_context)
        ),
        LlmMessage(
            role=LlmMessageRole.USER,
            content=get_knowledge_prompt()
        ),
    ]

    response = ai_service.chat_llm(chat).content

    json_data = json.loads(response)

    # ----------------------------
    # SAVE TO DATABASE
    # ----------------------------
    with SessionLocal() as session:
        with session.begin():

            knowledge = Knowledge(
                offer_id=offer_id,
                offer_summary=json_data.get("offer_summary", ""),
                category=json_data.get("category", ""),
                value_proposition=json_data.get("value_proposition", ""),
            )

            session.add(knowledge)
            session.flush()

            insight_items = []

            for field, insight_type in INSIGHT_MAPPING.items():

                items = json_data.get(field, [])

                if not isinstance(items, list):
                    items = [items]

                for item in items:

                    if not item:
                        continue

                    insight = KnowledgeInsight(
                        knowledge_id=knowledge.id,
                        type=insight_type,
                        value=str(item),
                        fact_status=FactStatus.VERIFIED.value,
                    )

                    insight_items.append(insight)

            session.add_all(insight_items)
            session.flush()

            for insight in insight_items:
                session.refresh(insight)

            session.refresh(knowledge)

            saved_insights = list(insight_items)


    # ----------------------------
    # PREPARE DTO RESULT
    # ----------------------------

    result = KnowledgeMapper.to_dto(
        knowledge
    )

    result.knowledge_insights = [
        KnowledgeInsightMapper.to_dto(item)
        for item in saved_insights
    ]

    return result



# =====================================================
# BASE ROLE
# =====================================================

def get_system_prompt() -> str:
    return """
You are a senior product strategist AI specialized in product analysis,
market research, customer psychology, and marketing strategy.

Your role is to deeply understand offers and transform raw offer
information into structured business knowledge.

Think like:
- a product manager,
- a market researcher,
- a growth strategist.

Rules:
- Understand before analyzing.
- Be specific to the offer.
- Avoid generic statements.
- Separate facts from assumptions.
- Make reasonable assumptions when data is incomplete.
- Focus on business value.

Return ONLY valid JSON.
Do not use markdown.
"""



# =====================================================
# KNOWLEDGE PROMPT
# =====================================================
def get_data_prompt( offer_context : str) -> str:
    return f"""
OFFER DATA:
    
{offer_context}
"""

# =====================================================
# KNOWLEDGE PROMPT
# =====================================================
def get_knowledge_prompt() -> str:
    return """
Analyze the offer information and create a deep understanding of this offer.

Your goal is to build a structured knowledge base that explains:
what this offer is, why it exists, what value it provides, and what makes it different.

Analyze the offer from the perspective of a senior product strategist.

Understand:

- What this offer actually is
- What category or market it belongs to
- What customer problem, need, or situation it addresses
- What solution it provides
- What transformation or outcome it creates
- Who it is potentially designed for
- Main components and elements included in the offer
- Key features
- Functional benefits
- Emotional benefits
- Value proposition
- Differentiation factors
- Strengths of the offer
- Possible weaknesses or limitations
- Important observations about the offer

Rules:

- Focus on understanding the offer itself.
- Do not create detailed customer personas yet.
- Do not create marketing campaigns or sales copy yet.
- Do not generate advertising messages yet.
- Separate facts from assumptions.
- If information is incomplete, make reasonable assumptions and clearly mark them.
- Add additional fields if they provide meaningful value for understanding the offer.
- Avoid generic statements. Stay specific to this offer.

Additional insight extraction rules:

- Extract the maximum possible number of meaningful insights about the offer.
- Do not limit the number of insights in any section.
- Lists do not need to contain the same number of elements.
- Some sections may contain many insights, while others may contain only a few or none if no meaningful information exists.
- Prioritize discovering valuable information over maintaining balanced output.
- Do not artificially create items just to fill sections.
- Include every relevant insight that can be logically derived from the offer information.

Important:
    - Do not create detailed personas.
    - Do not create advertising messages.
    - Do not create marketing campaigns.
    - Focus only on understanding the offer.
    - If something is uncertain, mark it as assumption.

Return ONLY valid JSON.

Use this structure as a foundation, but extend it when necessary:

{
    "offer_summary": "",
    "category": "",
    "problem_solved": [],
    "solution": [],
    "transformation": [],
    "offer_components": [],
    "features": [],
    "functional_benefits": [],
    "emotional_benefits": [],
    "value_proposition": "",
    "differentiators": [],
    "strengths": [],
    "limitations": [],
    "additional_insights": []
}
"""






