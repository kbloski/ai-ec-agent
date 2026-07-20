import json

from di.container import Container
from domain.models.ollama.llm_ollama_message import LlmOllamaMessage
from domain.enums.ollama_message_role import OllamaMessageRole


SYSTEM_PROMPT = """
Jesteś ekspertem od UGC (User Generated Content),
Performance Creative oraz Direct Response Advertising.


Twoim zadaniem jest stworzenie propozycji MATERIAŁÓW UGC
na podstawie pełnego kontekstu marketingowego.

NIE GENERUJ:

- finalnego scenariusza,
- gotowych dialogów,
- gotowych reklam,
- grafik,
- promptów wizualnych.



GENERUJ:


1. CREATOR PERSONA

Kto powinien nagrać materiał:

- typ twórcy,
- wiek,
- styl,
- dlaczego pasuje do marki.


2. FORMAT

Np. testimonial, unboxing, day-in-life, before/after, product demo, problem/solution.


3. ANGLE

Główny kąt komunikacji, na którym bazuje materiał.


4. HOOK IDEA

Pomysł na pierwsze sekundy nagrania.


5. SCRIPT OUTLINE

Ogólny szkic tego, co powinno się wydarzyć (bez pełnego copy):

- beats / etapy nagrania.


6. TONE OF VOICE

Ton, w jakim powinien mówić twórca.


7. PLATFORM FIT

Na jakie platformy/placementy pasuje materiał.


8. CTA

Sugerowane wezwanie do działania.


9. WHY IT SHOULD WORK

Uzasadnienie, dlaczego materiał powinien działać.



Zwróć wyłącznie JSON:


{
"ugc_creatives":[

{
"name":"",

"creator_persona":{
    "type":"",
    "age_range":"",
    "style":"",
    "why_it_fits":""
},

"format":"",

"angle":"",

"hook_idea":"",

"script_outline":[],

"tone_of_voice":"",

"platform_fit":[],

"cta":"",

"why_it_should_work":""
}

]
}


Bez markdown.
Bez komentarzy.
Tylko JSON.
"""


USER_PROMPT_TEMPLATE = """
Wygeneruj propozycje materiałów UGC na podstawie:


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


def generate_ugc_creatives_handler(
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


    def serialize(obj):
        return json.dumps(
            obj.to_dict(),
            ensure_ascii=False,
            indent=2,
            default=str
        )


    user_prompt = USER_PROMPT_TEMPLATE.format(

        knowledge_json=serialize(knowledge),

        brand_strategy_json=serialize(brand_strategy),

        marketing_strategy_json=serialize(marketing_strategy),

        offer_strategy_json=serialize(offer_strategy),

        message_strategy_json=serialize(message_strategy)

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

        return {
            "raw_response": response.content
        }


    return result.get("ugc_creatives", [])
