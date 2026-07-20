import json

from di.container import Container
from domain.models.ollama.llm_ollama_message import LlmOllamaMessage
from domain.enums.ollama_message_role import OllamaMessageRole


SYSTEM_PROMPT = """
Jesteś ekspertem od:

- Conversion Copywriting
- Direct Response Marketing
- Landing Page Copywriting
- Customer Psychology
- Persuasive Writing
- Offer Communication


Twoim zadaniem jest stworzenie PAGE COPY
na podstawie:

- Page Content Plan
- Page Strategy
- Message Strategy
- Offer Strategy


PAGE COPY jest finalną warstwą tekstową landing page.


Tworzysz:

- headline,
- subheadline,
- body_copy,
- bullet_points,
- CTA,
- supporting_text.


Nie tworzysz:

- strategii,
- struktury strony,
- nowych sekcji,
- HTML,
- CSS,
- React,
- komponentów,
- obrazów,
- promptów wizualnych.



ZASADY:


1. Używaj dokładnie sekcji przekazanych w PAGE CONTENT PLAN.


2. Nie dodawaj nowych sekcji.


3. Nie zmieniaj kolejności sekcji.


4. Każda sekcja musi realizować cel określony w PAGE CONTENT PLAN.


5. Copy musi:

- komunikować wartość produktu,
- odpowiadać na potrzeby klienta,
- usuwać obiekcje,
- zwiększać zaufanie,
- prowadzić do konwersji.


6. Nie wymyślaj nowych faktów.

Używaj wyłącznie informacji zawartych w dostarczonym kontekście.


7. Unikaj pustych fraz marketingowych.

Nie używaj:

- najlepszy produkt,
- numer jeden,
- rewolucyjny,
- przełomowy,
- wyjątkowy,
- niesamowity.



SECTION TYPE MUSI BYĆ JEDNYM Z:


hero
problem
solution
benefits
features
how_it_works
social_proof
testimonials
case_studies
comparison
offer
pricing
risk_reversal
objection_handling
faq
final_cta



OUTPUT FORMAT:


Zwróć dokładnie:


{
    "page_copy": {

        "sections": [

            {
                "order": 1,

                "section_type": "",

                "headline": "",

                "subheadline": "",

                "body_copy": "",

                "bullet_points": [],

                "cta": "",

                "supporting_text": ""

            }

        ]

    }
}



STRICT JSON RULES:


- zwróć wyłącznie JSON,
- używaj tylko standardowych podwójnych cudzysłowów ",
- nigdy nie używaj znaków „ ”,
- wszystkie klucze muszą być po angielsku,
- nie używaj markdown,
- nie używaj ```json,
- nie dodawaj komentarzy,
- nie dodawaj tekstu przed JSON,
- nie dodawaj tekstu po JSON,
- nie używaj null,
- bullet_points zawsze musi być tablicą,
- wszystkie pola muszą istnieć.
"""


USER_PROMPT_TEMPLATE = """
Wygeneruj Page Copy na podstawie:


KNOWLEDGE BASE:

{knowledge_json}


BRAND MARKETING:

{brand_marketing_json}


MARKETING STRATEGY:

{marketing_strategy_json}


PAGE BLUEPRINT:

{page_blueprint_json}


PAGE CONTENT PLAN:

{page_content_plan_json}


PAGE STRATEGY:

{page_strategy_json}


MESSAGE STRATEGY:

{message_strategy_json}


OFFER STRATEGY:

{offer_strategy_json}

"""


def normalize_json(content: str):

    replacements = {
        "„": '"',
        "”": '"',
        "‚": '"',
        "’": "'",
    }


    for old, new in replacements.items():

        content = content.replace(
            old,
            new
        )


    return content.strip()



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



def generate_page_copy_handler(
    knowledge_id: int,
    brand_marketing_id: int,
    marketing_strategy_id: int,
    offer_strategy_id: int,
    message_strategy_id: int,
    page_strategy_id: int,
    page_blueprint_id: int,
    page_content_plan_id: int
):

    container = Container()


    page_content_plan_service = (
        container.page_content_plan_service()
    )

    page_strategy_service = (
        container.page_strategy_service()
    )

    message_strategy_service = (
        container.message_strategy_service()
    )

    offer_strategy_service = (
        container.offer_strategy_service()
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

    page_blueprint_service = (
        container.page_blueprint_service()
    )


    ollama_service = (
        container.ollama_service()
    )



    page_content_plan = (
        page_content_plan_service
        .get_page_content_plan_by_id(
            id=page_content_plan_id
        )
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


    offer_strategy = (
        offer_strategy_service
        .get_offer_strategy_by_id(
            id=offer_strategy_id
        )
    )


    knowledge = (
        knowledge_service
        .get_knowledge_details_by_id(
            knowledge_id=knowledge_id
        )
    )


    brand_marketing = (
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


    page_blueprint = (
        page_blueprint_service
        .get_page_blueprint_by_id(
            id=page_blueprint_id
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

        brand_marketing_json=serialize(
            brand_marketing
        ),

        marketing_strategy_json=serialize(
            marketing_strategy
        ),

        page_blueprint_json=serialize(
            page_blueprint
        ),

        page_content_plan_json=serialize(
            page_content_plan
        ),

        page_strategy_json=serialize(
            page_strategy
        ),

        message_strategy_json=serialize(
            message_strategy
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


        content = normalize_json(
            content
        )


        result = json.loads(
            content
        )


        if isinstance(result, str):

            result = json.loads(
                result
            )



    except Exception as e:

        return {

            "error": "Invalid JSON response",

            "exception": str(e),

            "raw_response": response.content

        }



    if "page_copy" not in result:

        return {

            "error": "Missing page_copy object",

            "raw_response": response.content

        }



    if "sections" not in result["page_copy"]:

        return {

            "error": "Missing sections",

            "raw_response": response.content

        }



    return result