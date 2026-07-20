import json

from di.container import Container
from domain.models.ollama.llm_ollama_message import LlmOllamaMessage
from domain.enums.ollama_message_role import OllamaMessageRole
from domain.models.page_blueprint.page_blueprint import PageBlueprint


SYSTEM_PROMPT = """
Jesteś ekspertem od:

- Landing Page Architecture
- Conversion Rate Optimization
- Direct Response Marketing
- UX Psychology
- Marketing Asset Planning


Twoim zadaniem jest stworzenie PAGE BLUEPRINT
na podstawie:

- Knowledge Base
- Page Strategy
- Message Strategy
- Offer Strategy
- Marketing Context


Page Blueprint określa:

- jakie sekcje powinny znajdować się na stronie,
- jaka jest funkcja każdej sekcji,
- jaki cel konwersyjny realizuje,
- jakie elementy powinny zostać wygenerowane.


Nie tworzysz:

- finalnego copy,
- headline'ów,
- sloganów,
- HTML,
- CSS,
- React,
- finalnego designu,
- obrazów.


Page Blueprint odpowiada na pytanie:

"Jak powinna być zbudowana strona, aby przeprowadzić klienta od problemu do decyzji zakupowej?"


LOGIKA LANDING PAGE:


1. ATTENTION

Cel:
- zatrzymać uwagę,
- przekazać główną wartość.


2. PROBLEM AWARENESS

Cel:
- zwiększyć świadomość problemu.


3. SOLUTION AWARENESS

Cel:
- wyjaśnić rozwiązanie.


4. VALUE DEMONSTRATION

Cel:
- pokazać wartość.


5. TRUST BUILDING

Cel:
- zwiększyć wiarygodność.


6. OBJECTION REMOVAL

Cel:
- usunąć bariery zakupu.


7. CONVERSION

Cel:
- doprowadzić do działania.



FORMAT JSON:


{
    "page_blueprint": {

        "page_type": "",

        "primary_conversion_goal": "",

        "sections": [

            {
                "order": 1,

                "section_type": "",

                "section_priority": "",

                "purpose": "",

                "customer_journey_stage": "",

                "conversion_role": "",

                "psychological_goal": "",

                "required_elements": [],

                "proof_elements": [],

                "objection_targets": [],

                "notes": ""
            }

        ]

    }
}



AVAILABLE SECTION TYPES:


- hero

Cel:
Przyciągnięcie uwagi i komunikacja głównej wartości.


- problem

Cel:
Pokazanie problemu klienta i konsekwencji.


- solution

Cel:
Przedstawienie rozwiązania i jego mechanizmu.


- how_it_works

Cel:
Wyjaśnienie procesu działania produktu.


- benefits

Cel:
Pokazanie rezultatów i wartości dla klienta.


- features

Cel:
Przedstawienie funkcji produktu.


- comparison

Cel:
Pokazanie przewagi nad alternatywami.


- social_proof

Cel:
Budowanie wiarygodności.


- testimonials

Cel:
Pokazanie doświadczeń klientów.


- case_studies

Cel:
Pokazanie konkretnych rezultatów.


- objection_handling

Cel:
Usunięcie konkretnych barier zakupowych.


- faq

Cel:
Odpowiedź na najczęstsze pytania i obiekcje.


- offer

Cel:
Prezentacja wartości oferty.


- pricing

Cel:
Prezentacja ceny i wariantów zakupu.


- risk_reversal

Cel:
Zmniejszenie ryzyka zakupu.


- final_cta

Cel:
Doprowadzenie do konwersji.



ZASADY WYBORU SEKCJI:


Nie używaj wszystkich dostępnych sekcji.

Nie każdy landing page wymaga każdej sekcji.


Dobierz sekcje na podstawie:

- produktu,
- oferty,
- grupy docelowej,
- poziomu świadomości klienta,
- głównych obiekcji,
- celu konwersji.


Każda sekcja musi posiadać:

section_priority:


"required"

jeżeli sekcja jest niezbędna dla skuteczności strony.


"optional"

jeżeli sekcja może zwiększyć konwersję,
ale nie jest konieczna.


Nie twórz pustych sekcji.

Nie dodawaj sekcji tylko dlatego,
że znajduje się na liście AVAILABLE SECTION TYPES.


ZASADY:

- każda sekcja jest jednym obiektem JSON,
- nie twórz osobnych obiektów dla elementów sekcji,
- nie generuj copy,
- nie generuj designu,
- wszystkie pola muszą istnieć,
- nie używaj null.


Zwróć wyłącznie JSON.

Bez markdown.

Bez komentarzy.

Tylko JSON.
"""


USER_PROMPT_TEMPLATE = """
Wygeneruj Page Blueprint na podstawie:

KNOWLEDGE BASE:

{knowledge_json}


PAGE STRATEGY:

{page_strategy_json}


MESSAGE STRATEGY:

{message_strategy_json}


BRAND STRATEGY:

{brand_strategy_json}


MARKETING STRATEGY:

{marketing_strategy_json}


OFFER STRATEGY:

{offer_strategy_json}
"""


def generate_page_blueprint_handler(
    page_strategy_id: int
):

    container = Container()

    page_strategy_service = container.page_strategy_service()
    message_strategy_service = container.message_strategy_service()
    knowledge_service = container.knowledge_service()
    brand_marketing_service = container.brand_marketing_service()
    marketing_strategy_service = container.marketing_strategy_service()
    offer_strategy_service = container.offer_strategy_service()

    page_blueprint_repository = container.page_blueprint_repository()
    page_blueprint_service = container.page_blueprint_service()

    ollama_service = container.ollama_service()


    page_strategy = (
        page_strategy_service.get_page_strategy_by_id(
            id=page_strategy_id
        )
    )


    message_strategy = (
        message_strategy_service.get_message_strategy_by_id(
            id=page_strategy.message_strategy_id
        )
    )


    knowledge = (
        knowledge_service.get_knowledge_details_by_id(
            knowledge_id=message_strategy.knowledge_id
        )
    )


    brand_strategy = (
        brand_marketing_service.get_brand_marketing_by_id(
            id=message_strategy.brand_marketing_id
        )
    )


    marketing_strategy = (
        marketing_strategy_service.get_marketing_strategy_by_id(
            id=message_strategy.marketing_strategy_id
        )
    )


    offer_strategy = (
        offer_strategy_service.get_offer_strategy_by_id(
            id=message_strategy.offer_strategy_id
        )
    )


    def serialize(obj):
        return json.dumps(
            obj.to_dict(),
            ensure_ascii=False,
            indent=2,
            default=str
        )


    user_prompt = USER_PROMPT_TEMPLATE.format(
        knowledge_json=serialize(knowledge),
        page_strategy_json=serialize(page_strategy),
        message_strategy_json=serialize(message_strategy),
        brand_strategy_json=serialize(brand_strategy),
        marketing_strategy_json=serialize(marketing_strategy),
        offer_strategy_json=serialize(offer_strategy)
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


    try:
        content = response.content.strip()

        if content.startswith("```"):
            content = content.replace("```json", "")
            content = content.replace("```", "").strip()

        result = json.loads(content)

        if isinstance(result, str):
            result = json.loads(result)

    except Exception:
        return {
            "raw_response": response.content
        }


    page_blueprint_data = result.get("page_blueprint", {})

    entity = PageBlueprint(

        page_strategy_id=page_strategy_id,

        page_type=page_blueprint_data.get("page_type"),

        primary_conversion_goal=page_blueprint_data.get("primary_conversion_goal"),

        sections=page_blueprint_data.get("sections", []),

    )

    created = page_blueprint_repository.create(entity)

    return page_blueprint_service.get_page_blueprint_by_id(id=created.id)
