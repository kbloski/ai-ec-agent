import json

from di.container import Container
from domain.models.ollama.llm_ollama_message import LlmOllamaMessage
from domain.enums.ollama_message_role import OllamaMessageRole
from domain.models.page_copy.page_copy import PageCopy


SYSTEM_PROMPT = """
Jesteś ekspertem od:

- Conversion Copywriting
- Direct Response Marketing
- Landing Page Copy
- Customer Psychology


Twoim zadaniem jest stworzenie PAGE COPY
na podstawie:

- Page Content Plan
- Page Strategy
- Offer Strategy
- Message Strategy


Page Copy jest finalną warstwą tekstową landing page.

Tworzysz:

- headline,
- subheadline,
- body copy,
- bullet points,
- CTA,
- supporting text.


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


1. Używaj dokładnie sekcji przekazanych w Page Content Plan.


2. Nie dodawaj nowych sekcji.


3. Każda sekcja musi realizować cel określony w Page Content Plan.


4. Copy musi:

- komunikować wartość produktu,
- odpowiadać na potrzeby klienta,
- usuwać obiekcje,
- zwiększać zaufanie,
- prowadzić do konwersji.


5. Nie używaj pustych marketingowych fraz.


Unikaj:

- najlepszy produkt,
- rewolucyjny,
- numer jeden,
- przełomowa technologia.


6. Nie wymyślaj nowych faktów,
których nie ma w dostarczonym kontekście.



FORMAT JSON:


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



ZASADY JSON:

- wszystkie pola muszą istnieć,
- nie używaj null,
- nie używaj markdown,
- nie dodawaj komentarzy,
- zwróć tylko JSON.


"""


USER_PROMPT_TEMPLATE = """
Wygeneruj Page Copy na podstawie:


PAGE CONTENT PLAN:

{page_content_plan_json}


PAGE STRATEGY:

{page_strategy_json}


MESSAGE STRATEGY:

{message_strategy_json}


OFFER STRATEGY:

{offer_strategy_json}

"""


def generate_page_copy_handler(
    page_content_plan_id: int
):

    container = Container()

    page_content_plan_service = container.page_content_plan_service()
    page_blueprint_service = container.page_blueprint_service()
    page_strategy_service = container.page_strategy_service()
    message_strategy_service = container.message_strategy_service()
    offer_strategy_service = container.offer_strategy_service()

    page_copy_repository = container.page_copy_repository()
    page_copy_service = container.page_copy_service()

    ollama_service = container.ollama_service()


    page_content_plan = (
        page_content_plan_service.get_page_content_plan_by_id(
            id=page_content_plan_id
        )
    )


    page_blueprint = (
        page_blueprint_service.get_page_blueprint_by_id(
            id=page_content_plan.page_blueprint_id
        )
    )


    page_strategy = (
        page_strategy_service.get_page_strategy_by_id(
            id=page_blueprint.page_strategy_id
        )
    )


    message_strategy = (
        message_strategy_service.get_message_strategy_by_id(
            id=page_strategy.message_strategy_id
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

        content = response.content.strip()


        if content.startswith("```"):

            content = content.replace(
                "```json",
                ""
            )

            content = content.replace(
                "```",
                ""
            ).strip()



        result = json.loads(content)



        if isinstance(result, str):

            result = json.loads(result)



    except Exception:

        return {
            "raw_response": response.content
        }


    page_copy_data = result.get("page_copy", {})


    entity = PageCopy(

        page_content_plan_id=page_content_plan_id,

        sections=page_copy_data.get("sections", []),

    )


    created = page_copy_repository.create(entity)


    return page_copy_service.get_page_copy_by_id(id=created.id)
