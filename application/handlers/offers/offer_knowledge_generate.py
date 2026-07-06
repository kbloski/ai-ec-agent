import json

from di.container import Container
from domain.models.ollama.llm_ollama_message import LlmOllamaMessage
from domain.models.offers.offer_knowledge import OfferKnowledge
from domain.enums.ollama.ollama_message_role import OllamaMessageRole


def offer_knowledge_generate_handler(offer_id: int):
    container = Container()

    offers_repository = container.offers_repository()
    offer_items_repository = container.offer_items_repository()
    ollama_service = container.ollama_service()

    # 1. Load data
    offer = offers_repository.get_by_id(offer_id)

    if not offer:
        raise ValueError(f"Offer {offer_id} not found")

    offer_items = offer_items_repository.get_by_offer_id(offer_id)

    # 2. Build SAFE JSON for LLM (IMPORTANT FIX)
    offer_json = offer.to_dict() if hasattr(offer, "to_dict") else {
        "id": offer.id,
        "name": offer.name,
        "buying_price": float(offer.buying_price),
        "selling_price": float(offer.selling_price) if offer.selling_price else None,
        "details": offer.details,
        "target_audience": offer.target_audience,
        "pain_points": offer.pain_points,
    }

    offer_json["offer_items"] = [
        item.to_dict() if hasattr(item, "to_dict") else {
            "id": item.id,
            "name": item.name,
            "details": item.details,
            "quantity": getattr(item, "quantity", None),
        }
        for item in offer_items
    ] if offer_items else []

    # 3. SYSTEM PROMPT
    system_prompt = """
You are a product analyst AI.

Your task is to generate structured knowledge about the product.

Return ONLY valid JSON matching the schema.

OUTPUT SCHEMA:
{
  "product_understanding": "string",
  "market_analysis": "string",
  "unique_value": "string",
  "target_audience": [{
    "value": "string",
    "score": "float"
  }],
  "pain_points": [{
    "value": "string",
    "score": "float"
  }],
  "desires": [{
    "value": "string",
    "score": "float"
  }],
  "objections": [{
    "value": "string",
    "score": "float"
  }]
}

RULES:
- Do NOT repeat input fields verbatim
- Infer insights and expand meaning
- Be precise and marketing-oriented
- No markdown
- Output ONLY valid JSON
""".strip()

    # 4. USER PROMPT (FIX: clean JSON, no extra #)
    user_prompt = f"""
INPUT:
{json.dumps(offer_json, ensure_ascii=False)}
""".strip()

    # 5. BUILD CHAT
    chat = [
        LlmOllamaMessage(
            role=OllamaMessageRole.SYSTEM,
            content=system_prompt
        ),
        LlmOllamaMessage(
            role=OllamaMessageRole.USER,
            content=user_prompt
        ),
    ]

    # 6. CALL LLM
    response = ollama_service.chat_llm(chat)

    # 7. PARSE RESULT (SAFE)
    try:
        result = json.loads(response.content)
    except Exception:
        raise ValueError(f"Invalid JSON from LLM: {response}")

    # 8. SAVE TO DB
    # knowledge = OfferKnowledge(
    #     offer_id=offer_id,
    #     status="completed",
    #     product_understanding=result.get("product_understanding"),
    #     market_analysis=result.get("market_analysis"),
    #     target_audience=result.get("target_audience"),
    #     pain_points=result.get("pain_points"),
    #     desires=result.get("desires"),
    #     objections=result.get("objections"),
    #     unique_value=result.get("unique_value"),
    # )

    # container.offer_knowledge_repository().save(knowledge)

    return result