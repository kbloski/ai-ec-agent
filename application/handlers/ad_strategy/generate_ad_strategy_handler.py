import json

from di.container import Container
from domain.models.ollama.llm_ollama_message import LlmOllamaMessage
from domain.enums.ollama_message_role import OllamaMessageRole


SYSTEM_PROMPT = """
Jesteś ekspertem od Advertising Strategy,
Performance Marketing oraz Direct Response Marketing.

Twoim zadaniem jest stworzenie AD STRATEGY
na podstawie pełnego kontekstu marketingowego.

Twoim zadaniem jest odpowiedzieć:

"Jaką reklamę powinniśmy stworzyć,
dla kogo,
z jakim argumentem,
w jakim formacie
i dlaczego powinna działać?"

ŹRÓDŁA:

1. KNOWLEDGE BASE:

- oferta,
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
- tone,
- sposób komunikacji.



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



NIE GENERUJ:

- finalnego copy,
- headline'ów,
- scenariusza video,
- gotowych reklam,
- grafik,
- promptów wizualnych.



GENERUJ:


1. OBJECTIVE

Określ:

- business goal,
- advertising goal,
- conversion event.


2. CUSTOMER STAGE

Określ etap customer journey.


3. PRIORITY AUDIENCES

Określ:

- najważniejsze segmenty,
- kolejność testowania,
- dlaczego segment jest ważny.



4. AUDIENCE ANGLES

Dla każdego segmentu określ:

- pain point,
- desire,
- buying trigger.



5. MESSAGE ANGLES

Określ:

- główny argument,
- problem,
- promise,
- objection,
- wymagany proof.



6. OFFER ANGLES

Określ:

- sposób pokazania wartości,
- mechanizm wartości,
- redukcję ryzyka.



7. CREATIVE CONCEPTS

Stwórz pomysły,
które będą później rozwijane przez Creative Strategy.


Nie twórz scenariusza.

Określ:

- nazwę konceptu,
- ideę,
- bazujący message angle.



8. RECOMMENDED FORMATS

Określ jakie formaty reklam warto testować:

np:

- ugc_testimonial
- product_demo
- comparison
- founder_story
- before_after
- static_benefit_ad



9. TESTING HYPOTHESES

Twórz hipotezy eksperymentalne:

- co testujemy,
- wariant kontrolny,
- wariant testowy,
- metryka sukcesu.



Zwróć wyłącznie JSON:


{
    "objective": {
        "business_goal": "",
        "advertising_goal": "",
        "conversion_event": ""
    },


    "customer_stage": "",


    "priority_audiences": [

        {
            "segment": "",
            "priority": 1,
            "reason": ""
        }

    ],


    "audience_angles": [

        {
            "segment": "",

            "pain_point": "",

            "desire": "",

            "buying_trigger": ""
        }

    ],


    "message_angles": [

        {
            "angle": "",

            "problem": "",

            "promise": "",

            "objection": "",

            "proof_needed": ""
        }

    ],


    "offer_angles": [

        {
            "angle": "",

            "value_mechanism": "",

            "risk_reduction": ""
        }

    ],


    "creative_concepts": [

        {
            "name": "",

            "idea": "",

            "based_on_angle": ""
        }

    ],


    "recommended_formats": [

        {
            "format": "",

            "reason": ""
        }

    ],


    "testing_hypotheses": [

        {
            "hypothesis": "",

            "variable": "",

            "control": "",

            "variant": "",

            "metric": ""
        }

    ]
}



Bez markdown.
Bez komentarzy.
Tylko JSON.
"""


USER_PROMPT_TEMPLATE = """
Wygeneruj Ad Strategy na podstawie:


KNOWLEDGE BASE:

{knowledge_json}



BRAND STRATEGY:

{brand_strategy_json}



MARKETING STRATEGY:

{marketing_strategy_json}



OFFER STRATEGY:

{offer_strategy_json}



MESSAGE STRATEGY:

{message_strategy_json}

"""



def generate_ad_strategy_handler(
    knowledge_id: int,
    brand_marketing_id: int,
    marketing_strategy_id: int,
    offer_strategy_id: int,
    message_strategy_id: int
):

    container = Container()


    knowledge_service = container.knowledge_service()

    brand_marketing_service = (
        container.brand_marketing_service()
    )

    marketing_strategy_service = (
        container.marketing_strategy_service()
    )

    offer_strategy_service = (
        container.offer_strategy_service()
    )

    message_strategy_service = (
        container.message_strategy_service()
    )

    ollama_service = container.ollama_service()



    knowledge = (
        knowledge_service.get_knowledge_details_by_id(
            knowledge_id=knowledge_id
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


    message_strategy = (
        message_strategy_service.get_message_strategy_by_id(
            id=message_strategy_id
        )
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


    message_strategy_json = json.dumps(
        message_strategy.to_dict(),
        ensure_ascii=False,
        indent=2,
        default=str
    )



    user_prompt = USER_PROMPT_TEMPLATE.format(

        knowledge_json=knowledge_json,

        brand_strategy_json=brand_strategy_json,

        marketing_strategy_json=marketing_strategy_json,

        offer_strategy_json=offer_strategy_json,

        message_strategy_json=message_strategy_json

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

            content = (
                content
                .replace("```json", "")
                .replace("```", "")
                .strip()
            )


        result = json.loads(content)


    except json.JSONDecodeError:
        result = {
            "raw_response": response.content
        }

    return result