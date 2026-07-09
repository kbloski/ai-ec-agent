import json

from di.container import Container
from domain.models.ollama.llm_ollama_message import LlmOllamaMessage
from domain.enums.ollama_message_role import OllamaMessageRole


# =====================================================
# BASE ROLE
# =====================================================

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


# =====================================================
# STEP 1
# =====================================================

PRODUCT_UNDERSTANDING_PROMPT = """
Analyze the product information.

Build a deep understanding of the product.

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

Return:

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


# =====================================================
# STEP 2
# =====================================================

MARKET_ANALYSIS_PROMPT = """
Analyze the market context.

Use product understanding.

Analyze:

- Market category
- Customer segments
- Competitive positioning
- Market opportunities
- Market risks
- Alternative solutions customers currently use

Return:

{
    "market_category": "",
    "customer_segments": [],
    "competitive_positioning": "",
    "alternatives": [],
    "market_opportunities": [],
    "market_risks": []
}
"""


# =====================================================
# STEP 3
# =====================================================

CUSTOMER_ANALYSIS_PROMPT = """
Analyze customer psychology.

Use product understanding and market analysis.

Identify:

- Customer motivations
- Buying triggers
- Emotional drivers
- Customer fears
- Decision factors
- Reasons preventing purchase

Return:

{
    "customer_motivations": [],
    "buying_triggers": [],
    "emotional_drivers": [],
    "customer_fears": [],
    "decision_factors": []
}
"""


# =====================================================
# STEP 4
# =====================================================

ICP_GENERATION_PROMPT = """
Generate Ideal Customer Profiles.

Create realistic buyer profiles.

Analyze:

- Who they are
- Their situation
- Their needs
- Their problems
- Why they buy
- Purchase triggers

Avoid generic audiences.

Return:

{
    "customer_profiles": [
        {
            "name": "",
            "description": "",
            "situation": "",
            "needs": [],
            "problems": [],
            "purchase_trigger": "",
            "buying_motivation": ""
        }
    ]
}
"""


# =====================================================
# STEP 5
# =====================================================

JTBD_ANALYSIS_PROMPT = """
Analyze Jobs To Be Done.

Understand why customers hire this product.

Identify:

- Functional jobs
- Emotional jobs
- Social jobs
- Desired outcomes

Return:

{
    "jobs_to_be_done": [
        {
            "job": "",
            "situation": "",
            "motivation": "",
            "desired_outcome": ""
        }
    ]
}
"""


# =====================================================
# STEP 6
# =====================================================

MARKETING_ANGLES_PROMPT = """
Create marketing angles.

Use:

- Product understanding
- Customer psychology
- JTBD

Generate:

- Selling angles
- Emotional hooks
- Customer-focused messages

Return:

{
    "marketing_angles": [
        {
            "angle": "",
            "customer_problem": "",
            "message": "",
            "reason_it_works": ""
        }
    ]
}
"""


# =====================================================
# STEP 7
# =====================================================

INSIGHT_GENERATION_PROMPT = """
Generate final product insights.

Use:

- Product understanding
- Market analysis
- Customer psychology
- Customer profiles
- JTBD
- Marketing angles

Generate:

1. Target audience
2. Pain points
3. Desires
4. Objections
5. Buying triggers


Return:

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
    ],

    "buying_triggers": [
        {
            "value": "",
            "score": 0.0
        }
    ]
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

    try:
        return json.loads(response.content)

    except Exception:
        raise ValueError(
            f"Invalid JSON from LLM:\n{response.content}"
        )


# =====================================================
# MAIN PIPELINE
# =====================================================

def offer_knowledge_generate_handler(offer_id: int):

    container = Container()

    offers_repository = container.offers_repository()
    offer_items_repository = container.offer_items_repository()
    ollama_service = container.ollama_service()


    # ----------------------------
    # LOAD DATA
    # ----------------------------

    offer = offers_repository.get_by_id(offer_id)

    if not offer:
        raise ValueError(
            f"Offer {offer_id} not found"
        )


    offer_items = offer_items_repository.get_by_offer_id(
        offer_id
    )


    offer_json = (
        offer.to_dict()
        if hasattr(offer, "to_dict")
        else {
            "id": offer.id,
            "name": offer.name,
            "details": offer.details,
            "selling_price": float(offer.selling_price)
                if offer.selling_price else None,
        }
    )


    offer_json["offer_items"] = [
        item.to_dict()
        if hasattr(item, "to_dict")
        else {
            "name": item.name,
            "details": item.details,
        }
        for item in offer_items
    ]


    # ----------------------------
    # 1 PRODUCT UNDERSTANDING
    # ----------------------------

    product_understanding = call_llm(
        ollama_service,
        f"""
PRODUCT DATA:

{json.dumps(offer_json, ensure_ascii=False)}

TASK:

{PRODUCT_UNDERSTANDING_PROMPT}
"""
    )


    # ----------------------------
    # 2 MARKET ANALYSIS
    # ----------------------------

    market_analysis = call_llm(
        ollama_service,
        f"""
PRODUCT:

{json.dumps(product_understanding, ensure_ascii=False)}

TASK:

{MARKET_ANALYSIS_PROMPT}
"""
    )


    # ----------------------------
    # 3 CUSTOMER PSYCHOLOGY
    # ----------------------------

    customer_analysis = call_llm(
        ollama_service,
        f"""
PRODUCT:

{json.dumps(product_understanding, ensure_ascii=False)}

MARKET:

{json.dumps(market_analysis, ensure_ascii=False)}

TASK:

{CUSTOMER_ANALYSIS_PROMPT}
"""
    )


    # ----------------------------
    # 4 ICP
    # ----------------------------

    customer_profiles = call_llm(
        ollama_service,
        f"""
PRODUCT:

{json.dumps(product_understanding, ensure_ascii=False)}

CUSTOMER:

{json.dumps(customer_analysis, ensure_ascii=False)}

TASK:

{ICP_GENERATION_PROMPT}
"""
    )


    # ----------------------------
    # 5 JTBD
    # ----------------------------

    jtbd = call_llm(
        ollama_service,
        f"""
CUSTOMER PROFILES:

{json.dumps(customer_profiles, ensure_ascii=False)}

CUSTOMER ANALYSIS:

{json.dumps(customer_analysis, ensure_ascii=False)}

TASK:

{JTBD_ANALYSIS_PROMPT}
"""
    )


    # ----------------------------
    # 6 MARKETING ANGLES
    # ----------------------------

    marketing_angles = call_llm(
        ollama_service,
        f"""
PRODUCT:

{json.dumps(product_understanding, ensure_ascii=False)}

JTBD:

{json.dumps(jtbd, ensure_ascii=False)}

TASK:

{MARKETING_ANGLES_PROMPT}
"""
    )


    # ----------------------------
    # 7 FINAL INSIGHTS
    # ----------------------------

    insights = call_llm(
        ollama_service,
        f"""
PRODUCT:

{json.dumps(product_understanding, ensure_ascii=False)}

MARKET:

{json.dumps(market_analysis, ensure_ascii=False)}

CUSTOMER:

{json.dumps(customer_analysis, ensure_ascii=False)}

ICP:

{json.dumps(customer_profiles, ensure_ascii=False)}

JTBD:

{json.dumps(jtbd, ensure_ascii=False)}

MARKETING:

{json.dumps(marketing_angles, ensure_ascii=False)}

TASK:

{INSIGHT_GENERATION_PROMPT}
"""
    )


    return {
        "product_understanding": product_understanding,
        "market_analysis": market_analysis,
        "customer_analysis": customer_analysis,
        "customer_profiles": customer_profiles,
        "jtbd": jtbd,
        "marketing_angles": marketing_angles,
        "insights": insights,
    }