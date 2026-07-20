import json

from di.container import Container
from domain.models.ollama.llm_ollama_message import LlmOllamaMessage
from domain.enums.ollama_message_role import OllamaMessageRole
from domain.models.page_strategy.page_strategy import PageStrategy


SYSTEM_PROMPT = """
Jesteś ekspertem od:

- Conversion Rate Optimization
- Landing Page Strategy
- Customer Psychology
- Direct Response Marketing
- Marketing Strategy


Twoim zadaniem jest stworzenie PAGE STRATEGY
na podstawie pełnego kontekstu marketingowego.


Page Strategy definiuje:

- dlaczego landing page istnieje,
- do kogo mówi,
- jaki problem rozwiązuje,
- jaki komunikat prowadzi klienta do zakupu,
- jakie bariery trzeba usunąć,
- jakie argumenty zwiększają konwersję.


Nie tworzysz struktury strony.

Nie tworzysz sekcji landing page.

Nie tworzysz komponentów.

Nie tworzysz copy.

Nie tworzysz wizualizacji.



NIE GENERUJ:

- hero section,
- problem section,
- benefit section,
- FAQ,
- CTA placement,
- layout,
- HTML,
- CSS,
- React,
- headline'ów,
- sloganów,
- reklam.



Twoim zadaniem jest stworzenie strategii,
która będzie później użyta przez:

- Page Blueprint Generator,
- Copy Generator,
- Visual Generator,
- Frontend Generator.



ANALIZUJ:

1. CUSTOMER

Określ:

- kto jest odbiorcą,
- czego chce,
- czego się obawia,
- jakie ma bariery zakupowe.



2. POSITIONING

Określ:

- jak produkt powinien być pozycjonowany,
- jaka jest główna wartość,
- dlaczego klient powinien wybrać to rozwiązanie.



3. MESSAGE STRATEGY

Określ:

- główny komunikat,
- główny angle,
- emocjonalny motywator,
- racjonalne uzasadnienie.



4. CONVERSION STRATEGY

Określ:

- główny cel strony,
- pożądaną akcję użytkownika,
- największy czynnik konwersji,
- największe bariery konwersji.



5. CUSTOMER JOURNEY

Opisz:

- aktualny poziom świadomości klienta,
- drogę psychologiczną od problemu do decyzji.



FORMAT JSON:


{
    "page_strategy": {

        "goal": "",

        "conversion_action": "",


        "target_audience": "",

        "customer_awareness_level": "",

        "customer_journey_stage": "",


        "core_value_proposition": "",

        "main_message": "",

        "message_angle": "",


        "customer_problem": "",

        "customer_desire": "",


        "emotional_drivers": [
        ],


        "rational_drivers": [
        ],


        "purchase_motivators": [
        ],


        "purchase_barriers": [
        ],


        "objections_to_resolve": [
        ],


        "trust_requirements": [
        ],


        "competitive_positioning": "",


        "brand_voice_direction": "",


        "conversion_strategy": {

            "primary_conversion_driver": "",

            "secondary_conversion_drivers": [

            ],

            "decision_factors": [

            ]

        },


        "customer_journey_strategy": [

            {

                "stage": "",

                "customer_state": "",

                "marketing_goal": ""

            }

        ]

    }

}



ZASADY:

- wszystkie pola muszą istnieć,
- nie używaj null,
- nie pomijaj pól,
- nie generuj gotowego copy,
- nie generuj struktury strony,
- nie generuj elementów UI.


Zwróć wyłącznie JSON.

Bez markdown.

Bez komentarzy.

Tylko JSON.
"""


USER_PROMPT_TEMPLATE = """
Wygeneruj Page Strategy na podstawie:


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
    message_strategy_id: int
):

    container = Container()


    knowledge_service = container.knowledge_service()
    message_strategy_service = container.message_strategy_service()
    brand_marketing_service = container.brand_marketing_service()
    marketing_strategy_service = container.marketing_strategy_service()
    offer_strategy_service = container.offer_strategy_service()

    page_strategy_repository = container.page_strategy_repository()
    page_strategy_service = container.page_strategy_service()

    ollama_service = container.ollama_service()



    message_strategy = (
        message_strategy_service.get_message_strategy_by_id(
            id=message_strategy_id
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



    page_strategy_data = result.get("page_strategy", {})


    entity = PageStrategy(

        message_strategy_id=message_strategy_id,

        goal=page_strategy_data.get("goal"),

        conversion_action=page_strategy_data.get("conversion_action"),

        target_audience=page_strategy_data.get("target_audience"),

        customer_awareness_level=page_strategy_data.get("customer_awareness_level"),

        customer_journey_stage=page_strategy_data.get("customer_journey_stage"),

        core_value_proposition=page_strategy_data.get("core_value_proposition"),

        main_message=page_strategy_data.get("main_message"),

        message_angle=page_strategy_data.get("message_angle"),

        customer_problem=page_strategy_data.get("customer_problem"),

        customer_desire=page_strategy_data.get("customer_desire"),

        emotional_drivers=page_strategy_data.get("emotional_drivers", []),

        rational_drivers=page_strategy_data.get("rational_drivers", []),

        purchase_motivators=page_strategy_data.get("purchase_motivators", []),

        purchase_barriers=page_strategy_data.get("purchase_barriers", []),

        objections_to_resolve=page_strategy_data.get("objections_to_resolve", []),

        trust_requirements=page_strategy_data.get("trust_requirements", []),

        competitive_positioning=page_strategy_data.get("competitive_positioning"),

        brand_voice_direction=page_strategy_data.get("brand_voice_direction"),

        conversion_strategy=page_strategy_data.get("conversion_strategy"),

        customer_journey_strategy=page_strategy_data.get("customer_journey_strategy", []),

    )


    created = page_strategy_repository.create(entity)


    return page_strategy_service.get_page_strategy_by_id(id=created.id)
