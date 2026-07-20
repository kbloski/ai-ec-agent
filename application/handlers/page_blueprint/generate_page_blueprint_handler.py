import json

from di.container import Container
from domain.models.ollama.llm_ollama_message import LlmOllamaMessage
from domain.enums.ollama_message_role import OllamaMessageRole
from domain.models.page_blueprint.page_blueprint import PageBlueprint


SYSTEM_PROMPT = """
Stwórz PAGE BLUEPRINT landing page na podstawie dostarczonych danych:

- Knowledge Base
- Page Strategy
- Message Strategy
- Brand Strategy
- Marketing Strategy
- Offer Strategy


Page Blueprint określa:

- strukturę strony,
- kolejność sekcji,
- rolę konwersyjną każdej sekcji,
- elementy wymagane do wygenerowania później.


Nie generuj:

- finalnego copy,
- headline'ów,
- sloganów,
- designu,
- HTML/CSS,
- obrazów.


Celem strony jest przeprowadzenie użytkownika przez proces:

ATTENTION
→ PROBLEM AWARENESS
→ SOLUTION AWARENESS
→ VALUE
→ TRUST
→ OBJECTION REMOVAL
→ CONVERSION



SEKCJE LANDING PAGE:


REQUIRED SECTIONS:

Używaj ich w większości landing page sprzedażowych.


hero

Cel:
Pierwszy kontakt użytkownika ze stroną.
Przekazuje główną wartość.


problem

Cel:
Pokazuje problem klienta i konsekwencje.


solution

Cel:
Przedstawia rozwiązanie.


benefits

Cel:
Pokazuje rezultaty i wartość.


features

Cel:
Pokazuje elementy produktu/usługi.


how_it_works

Cel:
Wyjaśnia proces działania.


social_proof

Cel:
Buduje wiarygodność.


offer

Cel:
Prezentuje zakres oferty.


pricing

Cel:
Prezentuje cenę lub model zakupu.


risk_reversal

Cel:
Zmniejsza ryzyko zakupu.


objection_handling

Cel:
Usuwa bariery zakupowe.


faq

Cel:
Odpowiada na pytania.


final_cta

Cel:
Prowadzi do konwersji.



OPTIONAL SECTIONS:


comparison

Użyj gdy klient porównuje rozwiązania.


testimonials

Użyj gdy opinie klientów zwiększają zaufanie.


case_studies

Użyj gdy wyniki klientów są ważnym argumentem.


unique_mechanism

Użyj gdy produkt wymaga wyjaśnienia dlaczego działa.


before_after

Użyj gdy transformacja klienta jest kluczowa.


trust_bar

Użyj gdy potrzebne są dodatkowe dowody wiarygodności.


bonus_stack

Użyj gdy oferta posiada bonusy.


urgency

Użyj gdy istnieje realny powód szybkiej decyzji.



ZASADY WYBORU:


- Nie używaj wszystkich sekcji.
- Dodawaj tylko sekcje mające konkretną funkcję sprzedażową.
- Required oznacza sekcję niezbędną dla skuteczności strony.
- Optional oznacza sekcję zwiększającą konwersję, ale nie wymaganą.


OUTPUT FORMAT:


Zwróć dokładnie taki JSON:


{
    "page_blueprint": {

        "page_type": "",

        "primary_conversion_goal": "",

        "sections": [

            {
                "order": 1,

                "section_type": "",

                "section_priority": "required",

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



RESTRICTIONS:


- root JSON musi zawsze posiadać "page_blueprint"
- "page_blueprint" musi posiadać "sections"
- "sections" musi być tablicą
- każda sekcja musi być obiektem
- nie zwracaj tablicy jako root
- nie dodawaj żadnego tekstu przed JSON
- nie dodawaj żadnego tekstu po JSON
- nie używaj markdown
- nie używaj ```json
- wszystkie pola muszą istnieć
- nie używaj null
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


def extract_json(content: str):

    content = content.strip()

    if "```" in content:
        content = (
            content
            .replace("```json", "")
            .replace("```", "")
            .strip()
        )

    start = content.find("{")
    end = content.rfind("}")

    if start == -1 or end == -1:
        raise ValueError(
            "JSON object not found"
        )

    return content[start:end + 1]



def generate_page_blueprint_handler(
    knowledge_id: int,
    brand_marketing_id: int,
    marketing_strategy_id: int,
    offer_strategy_id: int,
    message_strategy_id: int,
    page_strategy_id: int
):

    container = Container()


    page_strategy_service = (
        container.page_strategy_service()
    )

    message_strategy_service = (
        container.message_strategy_service()
    )

    knowledge_service = (
        container.knowledge_service()
    )

    brand_marketing_service = (
        container.brand_marketing_service()
    )

    marketing_strategy_service = (
        container.marketing_strategy_service()
    )

    offer_strategy_service = (
        container.offer_strategy_service()
    )


    page_blueprint_repository = (
        container.page_blueprint_repository()
    )

    page_blueprint_service = (
        container.page_blueprint_service()
    )

    ollama_service = (
        container.ollama_service()
    )


    page_strategy = (
        page_strategy_service
        .get_page_strategy_by_id(
            id=page_strategy_id
        )
    )


    message_strategy = (
        message_strategy_service
        .get_message_strategy_by_id(
            id=message_strategy_id
        )
    )


    knowledge = (
        knowledge_service
        .get_knowledge_details_by_id(
            knowledge_id=knowledge_id
        )
    )


    brand_strategy = (
        brand_marketing_service
        .get_brand_marketing_by_id(
            id=brand_marketing_id
        )
    )


    marketing_strategy = (
        marketing_strategy_service
        .get_marketing_strategy_by_id(
            id=marketing_strategy_id
        )
    )


    offer_strategy = (
        offer_strategy_service
        .get_offer_strategy_by_id(
            id=offer_strategy_id
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

        knowledge_json=serialize(
            knowledge
        ),

        page_strategy_json=serialize(
            page_strategy
        ),

        message_strategy_json=serialize(
            message_strategy
        ),

        brand_strategy_json=serialize(
            brand_strategy
        ),

        marketing_strategy_json=serialize(
            marketing_strategy
        ),

        offer_strategy_json=serialize(
            offer_strategy
        )
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

        content = extract_json(
            response.content
        )

        result = json.loads(
            content
        )


    except Exception:

        return {

            "error": "Invalid JSON response",

            "raw_response": response.content

        }



    page_blueprint_data = (
        result.get(
            "page_blueprint",
            {}
        )
    )


    if not page_blueprint_data:

        return {

            "error": "Missing page_blueprint",

            "raw_response": response.content

        }


    sections = (
        page_blueprint_data.get(
            "sections",
            []
        )
    )


    if not isinstance(
        sections,
        list
    ):

        return {

            "error": "Sections must be list",

            "raw_response": response.content

        }



    entity = PageBlueprint(

        page_strategy_id=page_strategy_id,

        page_type=(
            page_blueprint_data.get(
                "page_type",
                ""
            )
        ),

        primary_conversion_goal=(
            page_blueprint_data.get(
                "primary_conversion_goal",
                ""
            )
        ),

        sections=sections

    )


    created = (
        page_blueprint_repository.create(
            entity
        )
    )


    return (
        page_blueprint_service
        .get_page_blueprint_by_id(
            id=created.id
        )
    )