import json

from di.container import Container
from domain.models.ollama.llm_ollama_message import LlmOllamaMessage
from domain.enums.ollama_message_role import OllamaMessageRole


SYSTEM_PROMPT = """
Jesteś ekspertem od tworzenia Offer Strategy.

Twoim zadaniem jest zaprojektowanie strategii oferty
na podstawie:

1. KNOWLEDGE BASE:
- oferta,
- klient,
- rynek,
- customer voice,
- problemy,
- potrzeby,
- obiekcje.

2. BRAND STRATEGY:
- positioning marki,
- wartości,
- osobowość,
- sposób postrzegania.

3. MARKETING STRATEGY:
- priorytetowe segmenty,
- kanały,
- customer journey,
- sposób zdobywania klientów.


Twoim zadaniem jest odpowiedzieć:

"Jak zapakować produkt w ofertę,
która będzie najbardziej atrakcyjna dla konkretnego klienta?"


Uwzględnij:

- wartość produktu,
- główny benefit,
- problemy klienta,
- redukcję ryzyka,
- elementy zwiększające konwersję,
- wyróżnienie względem konkurencji.


Nie generuj:
- reklam,
- headline'ów,
- copy,
- landing page,
- emaili.


Zwróć wyłącznie JSON:

{
    "offer_name": "",

    "offer_positioning": "",

    "core_value_proposition": "",

    "main_customer_problem": "",

    "solution_mechanism": "",

    "primary_benefit": "",

    "secondary_benefits": [],

    "functional_benefits": [],

    "emotional_benefits": [],

    "offer_structure": {},

    "value_stack": [],

    "risk_reversal": [],

    "trust_elements": [],

    "pricing_strategy": "",

    "urgency_strategy": "",

    "customer_objection_handling": [],

    "competitive_difference": "",

    "conversion_levers": []
}


Bez markdown.
Bez komentarzy.
Tylko JSON.
"""


USER_PROMPT_TEMPLATE = """
Wygeneruj Offer Strategy na podstawie danych.


KNOWLEDGE BASE:

{knowledge_json}


BRAND STRATEGY:

{brand_strategy_json}


MARKETING STRATEGY:

{marketing_strategy_json}

"""


def generate_offer_strategy_handler(
    knowledge_id: int,
    brand_marketing_id: int,
    marketing_strategy_id: int
):

    container = Container()

    knowledge_service = container.knowledge_service()
    brand_marketing_service = container.brand_marketing_service()
    marketing_strategy_service = container.marketing_strategy_service()
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


    user_prompt = USER_PROMPT_TEMPLATE.format(
        knowledge_json=knowledge_json,
        brand_strategy_json=brand_strategy_json,
        marketing_strategy_json=marketing_strategy_json
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


    return json.loads(response.content.strip())