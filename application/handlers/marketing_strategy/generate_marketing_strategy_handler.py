import json

from di.container import Container
from domain.models.ollama.llm_ollama_message import LlmOllamaMessage
from domain.enums.ollama_message_role import OllamaMessageRole


SYSTEM_PROMPT = """
Jesteś ekspertem od marketing strategy oraz growth marketingu.

Twoim zadaniem jest stworzenie strategii marketingowej na podstawie:

1. KNOWLEDGE BASE:
- produkt,
- rynek,
- konkurencja,
- customer voice,
- segmenty klientów,
- potrzeby,
- problemy,
- obiekcje.

2. CUSTOMER & MARKET INSIGHTS:
- dlaczego klient kupuje,
- czego potrzebuje,
- co blokuje zakup,
- jakie są najważniejsze motywacje.

3. BRAND STRATEGY:
- pozycjonowanie marki,
- osobowość,
- wartości,
- głos marki,
- percepcja klienta.

Twoim zadaniem jest określenie:

- jak zdobywać klientów,
- jakie kanały wykorzystać,
- jak wygląda customer journey,
- jakie działania marketingowe wykonywać,
- jak budować zaufanie,
- jakie segmenty priorytetyzować,
- jakie hipotezy testować.


Nie generujesz:
- reklam,
- headline'ów,
- tekstów sprzedażowych,
- landing page,
- emaili,
- kreacji.


Tworzysz strategię, która będzie później używana przez:
- offer strategy,
- message strategy,
- experiments,
- sales assets.


Zwróć wyłącznie poprawny JSON:

{
    "marketing_objective": "",

    "growth_strategy": "",

    "primary_audience": [
        ""
    ],

    "secondary_audience": [
        ""
    ],

    "audience_prioritization": [
        {
            "audience": "",
            "reason": "",
            "potential": ""
        }
    ],

    "customer_journey": {
        "awareness": "",
        "consideration": "",
        "conversion": "",
        "retention": ""
    },

    "marketing_channels": [
        {
            "channel": "",
            "role": "",
            "strategy": ""
        }
    ],

    "acquisition_strategy": [
        ""
    ],

    "trust_building_strategy": [
        ""
    ],

    "content_strategy": {
        "main_pillars": [
            ""
        ],
        "content_goals": [
            ""
        ]
    },

    "community_strategy": [
        ""
    ],

    "creator_influencer_strategy": [
        ""
    ],

    "campaign_directions": [
        {
            "name": "",
            "objective": "",
            "audience": "",
            "strategic_angle": ""
        }
    ],

    "conversion_strategy": [
        ""
    ],

    "retention_strategy": [
        ""
    ],

    "marketing_experiments": [
        {
            "hypothesis": "",
            "area": "",
            "success_metric": ""
        }
    ],

    "marketing_kpis": [
        ""
    ]
}


Nie dodawaj:
- markdown,
- ```json,
- komentarzy,
- tekstu przed JSON.
"""


USER_PROMPT_TEMPLATE = """
Wygeneruj marketing strategy na podstawie poniższych danych.

KNOWLEDGE BASE:

{knowledge_json}

BRAND STRATEGY:

{brand_strategy_json}
"""

# To na razie jest w knowledge 
# CUSTOMER & MARKET INSIGHTS:
# {insights_json}



def generate_marketing_strategy_handler(
    knowledge_id: int,
    brand_markeging_id: int
):
    container = Container()

    knowledge_service = container.knowledge_service()
    brand_marketing_service = container.brand_marketing_service()
    ollama_service = container.ollama_service()


    knowledge = knowledge_service.get_knowledge_details_by_id(
        knowledge_id=knowledge_id
    )

    brand_strategy = brand_marketing_service.get_brand_marketing_by_id(
        id=brand_markeging_id
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


    user_prompt = USER_PROMPT_TEMPLATE.format(
        knowledge_json=knowledge_json,
        brand_strategy_json=brand_strategy_json
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