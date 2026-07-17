import json

from di.container import Container
from domain.models.ollama.llm_ollama_message import LlmOllamaMessage
from domain.enums.ollama_message_role import OllamaMessageRole
from domain.models.message_strategy.message_strategy import MessageStrategy


SYSTEM_PROMPT = """
Jesteś ekspertem od Message Strategy oraz marketing communication strategy.

Twoim zadaniem jest stworzenie strategii komunikacji marki
na podstawie:

1. KNOWLEDGE BASE:
- produkt,
- klient,
- customer voice,
- problemy,
- potrzeby,
- obiekcje.

2. BRAND STRATEGY:
- positioning,
- wartości,
- osobowość marki,
- voice,
- tone.

3. MARKETING STRATEGY:
- segmenty klientów,
- kanały,
- customer journey,
- sposób dotarcia.

4. OFFER STRATEGY:
- wartość oferty,
- benefity,
- mechanizm rozwiązania,
- redukcja ryzyka,
- wyróżniki.


Twoim zadaniem jest określić:

- jakie komunikaty powinny być używane,
- jakie problemy klienta adresować,
- jakie emocje wykorzystywać,
- jakie argumenty racjonalne stosować,
- jak odpowiadać na obiekcje.


Nie generujesz:
- gotowych reklam,
- headline'ów,
- landing page,
- email copy.


Tworzysz fundament komunikacji,
który będzie używany przez generatory assetów.


Zwróć wyłącznie JSON:

{
    "core_message": "",

    "brand_message": "",

    "primary_message_angle": "",

    "secondary_message_angles": [],

    "audience_messages": [],

    "customer_pain_points": [],

    "customer_desires": [],

    "benefit_messages": [],

    "feature_to_benefit_mapping": [],

    "objection_handling_messages": [],

    "trust_messages": [],

    "proof_points": [],

    "emotional_triggers": [],

    "rational_arguments": [],

    "advertising_angles": [],

    "content_angles": [],

    "ugc_angles": []
}


Bez markdown.
Bez komentarzy.
Tylko JSON.
"""


USER_PROMPT_TEMPLATE = """
Wygeneruj Message Strategy na podstawie:


KNOWLEDGE BASE:

{knowledge_json}


BRAND STRATEGY:

{brand_strategy_json}


MARKETING STRATEGY:

{marketing_strategy_json}


OFFER STRATEGY:

{offer_strategy_json}

"""


def generate_message_strategy_handler(
    knowledge_id: int,
    brand_marketing_id: int,
    marketing_strategy_id: int,
    offer_strategy_id: int
):

    container = Container()

    knowledge_service = container.knowledge_service()
    brand_marketing_service = container.brand_marketing_service()
    marketing_strategy_service = container.marketing_strategy_service()
    offer_strategy_service = container.offer_strategy_service()
    message_strategy_repository = container.message_strategy_repository()
    message_strategy_service = container.message_strategy_service()

    ollama_service = container.ollama_service()


    knowledge = knowledge_service.get_knowledge_details_by_id(
        knowledge_id=knowledge_id
    )

    brand_strategy = brand_marketing_service.get_brand_marketing_by_id(
        id=brand_marketing_id
    )

    marketing_strategy = marketing_strategy_service.get_marketing_strategy_by_id(
        id=marketing_strategy_id
    )

    offer_strategy = offer_strategy_service.get_offer_strategy_by_id(
        id=offer_strategy_id
    )


    knowledge_json = json.dumps(
        knowledge.to_dict(),
        ensure_ascii=False,
        indent=2,
        default=str
    )

    brand_strategy_json = json.dumps(
        brand_strategy.to_dict(),
        ensure_ascii=False,
        indent=2,
        default=str
    )

    marketing_strategy_json = json.dumps(
        marketing_strategy.to_dict(),
        ensure_ascii=False,
        indent=2,
        default=str
    )

    offer_strategy_json = json.dumps(
        offer_strategy.to_dict(),
        ensure_ascii=False,
        indent=2,
        default=str
    )


    user_prompt = USER_PROMPT_TEMPLATE.format(
        knowledge_json=knowledge_json,
        brand_strategy_json=brand_strategy_json,
        marketing_strategy_json=marketing_strategy_json,
        offer_strategy_json=offer_strategy_json
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


    data = json.loads(response.content.strip())

    entity = MessageStrategy(
        knowledge_id=knowledge_id,
        brand_marketing_id=brand_marketing_id,
        marketing_strategy_id=marketing_strategy_id,
        offer_strategy_id=offer_strategy_id,
        core_message=data.get("core_message"),
        brand_message=data.get("brand_message"),
        primary_message_angle=data.get("primary_message_angle"),
        secondary_message_angles=data.get("secondary_message_angles", []),
        audience_messages=data.get("audience_messages", []),
        customer_pain_points=data.get("customer_pain_points", []),
        customer_desires=data.get("customer_desires", []),
        benefit_messages=data.get("benefit_messages", []),
        feature_to_benefit_mapping=data.get("feature_to_benefit_mapping", []),
        objection_handling_messages=data.get("objection_handling_messages", []),
        trust_messages=data.get("trust_messages", []),
        proof_points=data.get("proof_points", []),
        emotional_triggers=data.get("emotional_triggers", []),
        rational_arguments=data.get("rational_arguments", []),
        advertising_angles=data.get("advertising_angles", []),
        content_angles=data.get("content_angles", []),
        ugc_angles=data.get("ugc_angles", []),
    )
    created = message_strategy_repository.create(entity)

    return message_strategy_service.get_message_strategy_by_id(id=created.id)