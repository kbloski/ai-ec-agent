import json

from di.container import Container
from domain.models.ollama.llm_ollama_message import LlmOllamaMessage
from domain.enums.ollama.ollama_message_role import OllamaMessageRole


BASE_SYSTEM_PROMPT = """
You are a senior product strategist AI specialized in product analysis,
market research, customer psychology, and marketing strategy.

Your role is to deeply understand products and transform raw product
information into structured business insights.

Think like:
- a product manager,
- a market researcher,
- a growth strategist,
- a customer psychology expert.

Your principles:
- Understand before analyzing
- Be specific to the product
- Avoid generic marketing statements
- Separate facts from assumptions
- Make reasonable assumptions when data is incomplete
- Focus on business value and customer behavior

Always provide structured, precise, and actionable analysis.

Return ONLY valid JSON.
Do not use markdown.
Do not add explanations outside JSON.
"""


PRODUCT_UNDERSTANDING_PROMPT = """
Analyze the product information provided.

Your goal is to build a deep understanding of the product.

Analyze:
- What the product is
- What problem it solves
- Who it is designed for
- Main features
- Main benefits
- Value proposition
- Product differentiation

Focus only on understanding the product.
Do not generate customer insights yet.

Return JSON:
{
    "product_summary": "",
    "problem_solved": "",
    "solution": "",
    "features": [],
    "benefits": [],
    "value_proposition": "",
    "differentiators": []
}
"""


MARKET_ANALYSIS_PROMPT = """
Analyze the market context of the product.

Use the product understanding provided.

Analyze:
- Market category
- Potential customer segments
- Competitive positioning
- Market opportunities
- Possible risks
- Reasons why customers may choose this product

Return JSON:
{
    "market_category": "",
    "customer_segments": [],
    "competitive_positioning": "",
    "market_opportunities": [],
    "market_risks": []
}
"""


CUSTOMER_ANALYSIS_PROMPT = """
Analyze customer psychology for this product.

Use the product understanding and market analysis.

Identify:
- Customer motivations
- Buying triggers
- Emotional drivers
- Customer fears
- Decision factors
- Reasons preventing purchase

Return JSON:
{
    "customer_motivations": [],
    "buying_triggers": [],
    "emotional_drivers": [],
    "customer_fears": [],
    "decision_factors": []
}
"""


INSIGHT_GENERATION_PROMPT = """
Generate actionable product insights.

Use:
- Product understanding
- Market analysis
- Customer psychology

Generate:

1. Target audience:
Who is most likely to buy this product.

2. Pain points:
Problems, frustrations, and unmet needs.

3. Desires:
Expected outcomes, goals, and motivations.

4. Objections:
Reasons customers may hesitate before purchase.

Rules:
- Do not repeat previous analysis verbatim
- Generate specific insights
- Include reasonable assumptions when useful
- Focus on marketing usefulness

Return JSON:
{
    "target_audience": [
        {
            "value": "",
            "score": 0.0
        }
    ],
    "pain_points": [
        {
            "value": "",
            "score": 0.0
        }
    ],
    "desires": [
        {
            "value": "",
            "score": 0.0
        }
    ],
    "objections": [
        {
            "value": "",
            "score": 0.0
        }
    ]
}
"""


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

    try:
        return json.loads(response.content)
    except Exception:
        raise ValueError(
            f"Invalid JSON from LLM: {response.content}"
        )


def offer_knowledge_generate_handler(offer_id: int):
    container = Container()

    offers_repository = container.offers_repository()
    offer_items_repository = container.offer_items_repository()
    ollama_service = container.ollama_service()

    # 1. Load offer data
    offer = offers_repository.get_by_id(offer_id)

    if not offer:
        raise ValueError(f"Offer {offer_id} not found")

    offer_items = offer_items_repository.get_by_offer_id(offer_id)

    offer_json = offer.to_dict() if hasattr(offer, "to_dict") else {
        "id": offer.id,
        "name": offer.name,
        "buying_price": float(offer.buying_price),
        "selling_price": float(offer.selling_price)
            if offer.selling_price else None,
        "details": offer.details,
        "target_audience": offer.target_audience,
        "pain_points": offer.pain_points,
    }

    offer_json["offer_items"] = [
        item.to_dict()
        if hasattr(item, "to_dict")
        else {
            "id": item.id,
            "name": item.name,
            "details": item.details,
            "quantity": getattr(item, "quantity", None),
        }
        for item in offer_items
    ]

    # ----------------------------------
    # STEP 1 - PRODUCT UNDERSTANDING
    # ----------------------------------

    product_understanding = call_llm(
        ollama_service,
        f"""
PRODUCT DATA:

{json.dumps(offer_json, ensure_ascii=False)}

TASK:

{PRODUCT_UNDERSTANDING_PROMPT}
"""
    )


    # ----------------------------------
    # STEP 2 - MARKET ANALYSIS
    # ----------------------------------

    market_analysis = call_llm(
        ollama_service,
        f"""
PRODUCT UNDERSTANDING:

{json.dumps(product_understanding, ensure_ascii=False)}

TASK:

{MARKET_ANALYSIS_PROMPT}
"""
    )


    # ----------------------------------
    # STEP 3 - CUSTOMER PSYCHOLOGY
    # ----------------------------------

    customer_analysis = call_llm(
        ollama_service,
        f"""
PRODUCT UNDERSTANDING:

{json.dumps(product_understanding, ensure_ascii=False)}


MARKET ANALYSIS:

{json.dumps(market_analysis, ensure_ascii=False)}


TASK:

{CUSTOMER_ANALYSIS_PROMPT}
"""
    )


    # ----------------------------------
    # STEP 4 - INSIGHTS
    # ----------------------------------

    insights = call_llm(
        ollama_service,
        f"""
PRODUCT UNDERSTANDING:

{json.dumps(product_understanding, ensure_ascii=False)}


MARKET ANALYSIS:

{json.dumps(market_analysis, ensure_ascii=False)}


CUSTOMER PSYCHOLOGY:

{json.dumps(customer_analysis, ensure_ascii=False)}


TASK:

{INSIGHT_GENERATION_PROMPT}
"""
    )


    return {
        "product_understanding": product_understanding,
        "market_analysis": market_analysis,
        "customer_analysis": customer_analysis,
        "insights": insights,
    }