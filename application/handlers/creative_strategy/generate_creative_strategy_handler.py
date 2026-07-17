import json

from di.container import Container

from domain.models.ollama.llm_ollama_message import LlmOllamaMessage
from domain.enums.ollama_message_role import OllamaMessageRole

from domain.models.creative_strategy.creative_strategy import CreativeStrategy



SYSTEM_PROMPT = """
Jesteś ekspertem od Performance Creative,
Direct Response Advertising,
Video Advertising oraz Creative Production.


Twoim zadaniem jest stworzenie CREATIVE STRATEGY
na podstawie pełnego kontekstu marketingowego i Ad Strategy.


CREATIVE STRATEGY jest dokumentem produkcyjnym reklamy.


Tworzysz kompletny blueprint reklamy:


- wygląd reklamy,
- sposób nagrania,
- strukturę,
- sceny,
- tekst,
- assety produkcyjne.


================================
PARAMETRY REKLAMY
================================


Parametry reklamy przekazane w USER PROMPT są obowiązkowe.


Musisz zachować:

- platformę,
- format,
- aspect ratio,
- długość reklamy.


Jeżeli długość reklamy wynosi X sekund:


1. execution.duration musi wynosić X sekund.

2. Wszystkie sceny w script muszą razem mieć dokładnie X sekund.

3. Każda scena musi mieć realny czas trwania.

4. Nie dodawaj dodatkowych sekund poza określony czas.

5. Dopasuj liczbę scen do długości reklamy.


Przykład:


Dla reklamy 30 sekund:


script:

scene 1:
5 sekund

scene 2:
10 sekund

scene 3:
10 sekund

scene 4:
5 sekund


SUMA = 30 sekund



================================
ŹRÓDŁA
================================


KNOWLEDGE BASE

- produkt
- klient
- problemy
- potrzeby
- obiekcje


MESSAGE STRATEGY

- komunikaty
- argumenty
- proof points


AD STRATEGY

- audience
- angle
- objective
- creative concepts



================================
GENERUJ
================================


1. CREATIVE EXECUTION


Pola:

- platform
- format
- duration
- aspect_ratio
- creative_type
- production_style
- camera_style
- editing_style
- voice_style



2. SCRIPT STRUCTURE


Nie generuj ogólnej historii.


Generuj konkretne sceny reklamowe.


Każda scena:


- order
- duration_seconds
- purpose
- visual
- dialogue
- voiceover
- on_screen_text
- emotion



3. ASSET REQUIREMENTS


Określ:

- video shots
- images
- product shots
- testimonials
- screenshots
- animations



4. PRODUCTION NOTES


Pola:

- shooting_notes
- editing_notes
- important_details



5. CTA


Pola:

- goal
- action_type
- placement



================================
NIE GENERUJ
================================


- grafik
- video
- promptów AI
- gotowych assetów



================================
FORMAT ODPOWIEDZI
================================


Zwróć tylko JSON.

Bez markdown.
Bez komentarzy.



Format:


{
"creative_strategies":[

{

"name":"",


"execution":{

"platform":"",
"format":"",
"duration_seconds":30,
"aspect_ratio":"",
"creative_type":"",
"production_style":"",
"camera_style":"",
"editing_style":"",
"voice_style":""

},


"script":[

{

"order":1,
"duration_seconds":5,
"purpose":"",
"visual":"",
"dialogue":"",
"voiceover":"",
"on_screen_text":"",
"emotion":""

}

],


"asset_requirements":[

{

"type":"",
"description":"",
"purpose":""

}

],


"production_notes":{

"shooting_notes":"",
"editing_notes":"",
"important_details":""

},


"cta":{

"goal":"",
"action_type":"",
"placement":""

}


}

]

}

"""



USER_PROMPT_TEMPLATE = """

================================
PARAMETRY REKLAMY
================================


Platform:

{platform}


Format:

{format}


Maksymalna długość reklamy:

{video_duration_seconds} sekund



================================
GENERUJ CREATIVE STRATEGY
================================



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



AD STRATEGY:

{ad_strategy_json}

"""



def generate_creative_strategy_handler(

    knowledge_id: int,

    brand_marketing_id: int,

    marketing_strategy_id: int,

    offer_strategy_id: int,

    message_strategy_id: int,

    ad_strategy_id: int,


    video_duration_seconds: int = 17,

    platform: str = "Meta Ads",

    format: str = "Vertical Video 9:16"

):


    container = Container()



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


    message_strategy_service = (
        container.message_strategy_service()
    )


    ad_strategy_service = (
        container.ad_strategy_service()
    )



    creative_strategy_repository = (
        container.creative_strategy_repository()
    )


    creative_strategy_service = (
        container.creative_strategy_service()
    )


    ollama_service = (
        container.ollama_service()
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


    message_strategy = (
        message_strategy_service
        .get_message_strategy_by_id(
            id=message_strategy_id
        )
    )


    ad_strategy = (
        ad_strategy_service
        .get_ad_strategy_by_id(
            id=ad_strategy_id
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

        platform=platform,

        format=format,

        video_duration_seconds=video_duration_seconds,


        knowledge_json=serialize(
            knowledge
        ),


        brand_strategy_json=serialize(
            brand_strategy
        ),


        marketing_strategy_json=serialize(
            marketing_strategy
        ),


        offer_strategy_json=serialize(
            offer_strategy
        ),


        message_strategy_json=serialize(
            message_strategy
        ),


        ad_strategy_json=serialize(
            ad_strategy
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


            content = (

                content

                .replace(
                    "```json",
                    ""
                )

                .replace(
                    "```",
                    ""
                )

                .strip()

            )



        result = json.loads(
            content
        )



    except json.JSONDecodeError:


        return {

            "raw_response": response.content

        }




    created_ids = []



    strategies = result.get(

        "creative_strategies",

        []

    )




    for item in strategies:



        execution = item.get(
            "execution",
            {}
        )


        script = item.get(
            "script",
            []
        )



        # dodatkowa kontrola długości reklamy

        total_duration = sum(

            scene.get(
                "duration_seconds",
                0
            )

            for scene in script

        )



        if total_duration != video_duration_seconds:


            raise ValueError(

                f"Generated script duration "
                f"{total_duration}s does not match "
                f"required {video_duration_seconds}s"

            )




        entity = CreativeStrategy(



            knowledge_id=knowledge_id,


            brand_marketing_id=brand_marketing_id,


            marketing_strategy_id=marketing_strategy_id,


            offer_strategy_id=offer_strategy_id,


            message_strategy_id=message_strategy_id,


            ad_strategy_id=ad_strategy_id,



            name=item.get(
                "name"
            ),



            execution=execution,



            script=script,



            asset_requirements=item.get(

                "asset_requirements",

                []

            ),



            production_notes=item.get(

                "production_notes"

            ),



            cta=item.get(

                "cta"

            )

        )




        created = (

            creative_strategy_repository

            .create(

                entity

            )

        )



        created_ids.append(

            created.id

        )




    return [

        creative_strategy_service

        .get_creative_strategy_by_id(

            id=id

        )

        for id in created_ids

    ]