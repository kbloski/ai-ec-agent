import json

from di.container import Container
from domain.models.ollama.llm_ollama_message import LlmOllamaMessage
from domain.enums.ollama.ollama_message_role import OllamaMessageRole

from domain.models.offers.offer_knowledge import OfferKnowledge
from domain.models.offers.offer_insight import OfferInsight

from domain.enums.offers.offer_knowledge_status import OfferKnowledgeStatus
from domain.enums.offers.offer_insight_type import OfferInsightType
from domain.enums.offers.offer_insight_status import OfferInsightStatus

from infrastructure.database.db import SessionLocal


# =====================================================
# BASE ROLE
# =====================================================

BASE_SYSTEM_PROMPT = """
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
# OFFER KNOWLEDGE PROMPT
# =====================================================
# OFFER_KNOWLEDGE_PROMPT = """
# Analyze the offer information and create a deep understanding of this offer.

# Your goal is to build a structured knowledge base that explains:
# what this offer is, why it exists, what value it provides, and what makes it different.

# Analyze the offer from the perspective of a senior product strategist.

# Understand:

# - What this offer actually is
# - What category or market it belongs to
# - What customer problem, need, or situation it addresses
# - What solution it provides
# - What transformation or outcome it creates
# - Who it is potentially designed for
# - Main components and elements included in the offer
# - Key features
# - Functional benefits
# - Emotional benefits
# - Value proposition
# - Differentiation factors
# - Strengths of the offer
# - Possible weaknesses or limitations
# - Important observations about the offer

# Rules:

# - Focus on understanding the offer itself.
# - Do not create detailed customer personas yet.
# - Do not create marketing campaigns or sales copy yet.
# - Do not generate advertising messages yet.
# - Separate facts from assumptions.
# - If information is incomplete, make reasonable assumptions and clearly mark them.
# - Add additional fields if they provide meaningful value for understanding the offer.
# - Avoid generic statements. Stay specific to this offer.


# Important:
#     - Do not create detailed personas.
#     - Do not create advertising messages.
#     - Do not create marketing campaigns.
#     - Focus only on understanding the offer.
#     - If something is uncertain, mark it as assumption.

# Return ONLY valid JSON.

# Use this structure as a foundation, but extend it when necessary:

# {
#     "offer_summary": "",
#     "category": "",
#     "problem_solved": [],
#     "solution": [],
#     "transformation": [],

#     "offer_components": [],

#     "features": [],
#     "functional_benefits": [],
#     "emotional_benefits": [],

#     "value_proposition": "",

#     "differentiators": [],

#     "strengths": [],
#     "limitations": [],

#     "assumptions": [],

#     "additional_insights": []
# }
# """


OFFER_KNOWLEDGE_PROMPT = """
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

    "assumptions": [],

    "additional_insights": []
}
"""








# =====================================================
# LLM CALL
# =====================================================

def call_llm(ollama_service, prompt):

    chat = [
        LlmOllamaMessage(
            role=OllamaMessageRole.SYSTEM,
            content=BASE_SYSTEM_PROMPT
        ),
        LlmOllamaMessage(
            role=OllamaMessageRole.USER,
            content=prompt
        ),
    ]

    response = ollama_service.chat_llm(chat)

    return response.content



# =====================================================
# INSIGHT TYPE MAPPING
# =====================================================

INSIGHT_MAPPING = {
    "problem_solved": OfferInsightType.PROBLEM_SOLVED,
    "solution":OfferInsightType.SOLUTION,
    "transformation":OfferInsightType.TRANSFORMATION,
    "offer_components":OfferInsightType.OFFER_COMPONENT,
    "features":OfferInsightType.FEATURE,
    "functional_benefits":OfferInsightType.FUNCTIONAL_BENEFIT,
    "emotional_benefits":OfferInsightType.EMOTIONAL_BENEFIT,
    "differentiators":OfferInsightType.DIFFERENTIATOR,
    "strengths":OfferInsightType.STRENGTH,
    "limitations":OfferInsightType.LIMITATION,
    "assumptions":OfferInsightType.ASSUMPTION,
    "additional_insights":OfferInsightType.ADDITIONAL_INSIGHT,
}



# =====================================================
# MAIN HANDLER
# =====================================================

def offer_knowledge_generate_handler(offer_id: int):

    container = Container()

    offers_repository = container.offers_repository()
    offer_items_repository = container.offer_items_repository()
    ollama_service = container.ollama_service()


    # ----------------------------
    # LOAD OFFER
    # ----------------------------
    offer = offers_repository.get_by_id( offer_id)

    if not offer:
        raise ValueError(
            f"Offer {offer_id} not found"
        )


    offer_items = offer_items_repository.get_by_offer_id(offer_id)


    offer_json = (
        offer.to_dict()
        if hasattr(offer, "to_dict")
        else {
            "id": offer.id,
            "name": offer.name,
            "details": offer.details,
            "selling_price": float(
                offer.selling_price
            )
            if offer.selling_price else None,
        }
    )

    offer_json["offer_items"] = [ item.to_dict() for item in offer_items ]


    # ----------------------------
    # GENERATE KNOWLEDGE
    # ----------------------------

    response = call_llm(
        ollama_service,

        f"""
OFFER DATA:

{json.dumps(
    offer_json,
    ensure_ascii=False
)}

TASK:

{OFFER_KNOWLEDGE_PROMPT}

"""
    )


    json_data = json.loads(response)



    # ----------------------------
    # SAVE TO DATABASE
    # ----------------------------
    with SessionLocal() as session:
        with session.begin():
            offer_knowledge = OfferKnowledge(
                offer_id=offer_id,
                version=1,
                status=OfferKnowledgeStatus.COMPLETED,
                offer_summary=json_data.get( "offer_summary",  "" ),
                category=json_data.get("category", ""),
                value_proposition=json_data.get( "value_proposition", "" ),
            )

            session.add(  offer_knowledge )
            session.flush()

            # ----------------------------
            # SAVE INSIGHTS
            # ----------------------------

            insight_items = []
            for field, insight_type in INSIGHT_MAPPING.items():

                items = json_data.get(field, [])

                if not isinstance(items, list):
                    items = [items]


                for item in items:
                    value = item
     

                    if not value:
                        continue

                    insight = OfferInsight(
                        offer_id=offer_id,
                        knowledge_id=offer_knowledge.id,
                        type=insight_type,
                        value=str(value),
                        status=OfferInsightStatus.APPROVED,
                    )

                    insight_items.append(insight)


            session.add_all(insight_items)


    return json_data