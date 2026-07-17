import json

from di.container import Container
from domain.models.ollama.llm_ollama_message import LlmOllamaMessage
from domain.enums.ollama_message_role import OllamaMessageRole


SYSTEM_PROMPT = """
Jesteś ekspertem od Conversion Rate Optimization,
Landing Page Strategy oraz Marketing Asset Architecture.

Twoim zadaniem jest stworzenie struktury landing page
na podstawie pełnego kontekstu marketingowego.


ŹRÓDŁA DANYCH:

1. KNOWLEDGE BASE:
- produkt,
- customer voice,
- problemy klientów,
- potrzeby,
- motywacje zakupowe,
- obiekcje,
- rynek,
- konkurencja.


2. BRAND STRATEGY:
- positioning,
- wartości marki,
- osobowość marki,
- voice,
- tone.


3. MARKETING STRATEGY:
- segmenty klientów,
- kanały,
- customer journey,
- sposób dotarcia.


4. OFFER STRATEGY:
- value proposition,
- mechanizm wartości,
- benefity,
- pricing angle,
- redukcja ryzyka,
- wyróżniki.


5. MESSAGE STRATEGY:
- core message,
- message angles,
- customer pains,
- customer desires,
- benefit messages,
- objection handling,
- proof points,
- emotional triggers.



TWOJE ZADANIE:

Wygeneruj strukturę landing page, która będzie podstawą dla:

- frontend generatora,
- copy generatora,
- visual generation engine,
- marketing asset engine.



GENERUJ:

1. PAGE STRATEGY

- cel strony,
- główny komunikat,
- grupa docelowa,
- customer journey stage,
- conversion goal.



2. PAGE SECTIONS

Każda sekcja musi zawierać:

- order,
- section_type,
- purpose,
- headline,
- subheadline,
- content,
- CTA,
- objections addressed,
- message angle,
- emotional trigger,
- rational argument,
- visual requirements.



Dostępne typy sekcji:

hero,
problem,
solution,
how_it_works,
benefits,
features,
comparison,
social_proof,
testimonials,
case_studies,
objection_handling,
faq,
offer,
pricing,
risk_reversal,
final_cta



3. VISUALIZATION PLAN

Nie generuj obrazów.

Określ tylko:

- jakie wizualizacje są potrzebne,
- gdzie powinny wystąpić,
- jaki mają cel,
- jaki powinien być kierunek generowania.



NIE GENERUJ:

- HTML,
- CSS,
- komponentów frontendowych,
- finalnego designu,
- gotowych obrazów.



Zwróć wyłącznie JSON.

Bez markdown.
Bez komentarzy.
Tylko JSON.
"""


USER_PROMPT_TEMPLATE = """
Wygeneruj strukturę landing page na podstawie:


KNOWLEDGE BASE:

{knowledge_json}


MESSAGE STRATEGY:

{message_strategy_json}


BRAND STRATEGY:

{brand_strategy_json}


MARKETING STRATEGY:

{marketing_strategy_json}


OFFER STRATEGY:

{offer_strategy_json}

"""


def generate_page_strategy_json_handler(
    knowledge_id: int,
    message_strategy_id: int,
    brand_marketing_id: int,
    marketing_strategy_id: int,
    offer_strategy_id: int
):

    container = Container()


    knowledge_service = container.knowledge_service()
    message_strategy_service = container.message_strategy_service()
    brand_marketing_service = container.brand_marketing_service()
    marketing_strategy_service = container.marketing_strategy_service()
    offer_strategy_service = container.offer_strategy_service()

    ollama_service = container.ollama_service()


    knowledge = (
        knowledge_service.get_knowledge_details_by_id(
            knowledge_id=knowledge_id
        )
    )


    message_strategy = (
        message_strategy_service.get_message_strategy_by_id(
            id=message_strategy_id
        )
    )


    brand_strategy = (
        brand_marketing_service.get_brand_marketing_by_id(
            id=brand_marketing_id
        )
    )


    marketing_strategy = (
        marketing_strategy_service.get_marketing_strategy_by_id(
            id=marketing_strategy_id
        )
    )


    offer_strategy = (
        offer_strategy_service.get_offer_strategy_by_id(
            id=offer_strategy_id
        )
    )



    knowledge_json = json.dumps(
        knowledge.to_dict(),
        ensure_ascii=False,
        indent=2,
        default=str
    )


    message_strategy_json = json.dumps(
        message_strategy.to_dict(),
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
        message_strategy_json=message_strategy_json,
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


    result = json.loads(
        response.content.strip()
    )


    # lineage metadata
    # result["metadata"] = {
    #     "knowledge_id": knowledge_id,
    #     "message_strategy_id": message_strategy_id,
    #     "brand_marketing_id": brand_marketing_id,
    #     "marketing_strategy_id": marketing_strategy_id,
    #     "offer_strategy_id": offer_strategy_id
    # }


    return result