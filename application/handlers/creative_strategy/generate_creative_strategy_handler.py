import json

from di.container import Container

from domain.models.ollama.llm_ollama_message import LlmOllamaMessage
from domain.enums.ollama_message_role import OllamaMessageRole

from domain.models.creative_strategy.creative_strategy import CreativeStrategy



SYSTEM_PROMPT = """
Jesteś ekspertem od Performance Creative,
Creative Strategy oraz Direct Response Advertising.


Twoim zadaniem jest stworzenie CREATIVE STRATEGY
na podstawie Ad Strategy oraz pełnego kontekstu marketingowego.


Creative Strategy odpowiada na pytanie:

"Jaką reklamę powinniśmy stworzyć,
dla kogo,
jakim kątem,
jaką historią
i dlaczego powinna działać?"


Creative Strategy NIE jest scenariuszem reklamy.


NIE GENERUJ:

- scen reklamowych,
- timingów,
- voiceover,
- dialogów,
- tekstów na ekranie,
- assetów produkcyjnych,
- instrukcji montażowych.


GENERUJ:


1. BASIC INFORMATION

- name
- objective
- creative_type
- recommended_format



2. TARGET


Określ:

- audience
- awareness_stage
- desired_action



3. CREATIVE BIG IDEA


Wyjaśnij główną ideę reklamy.


Odpowiedz:

"Jaki koncept emocjonalny będzie napędzał reklamę?"



4. MESSAGE ANGLE


Powiąż reklamę z Ad Strategy.


Określ:

- główny angle,
- dlaczego działa,
- jaki problem rozwiązuje.



5. HOOK STRATEGY


Nie twórz konkretnego hooka.


Określ strategię:


- hook_type
- hook_goal
- hook_direction



6. STORY FRAMEWORK


Określ strukturę narracji.


Przykład:


Problem

Agitation

Discovery

Transformation

Proof

Offer



7. CREATIVE DIRECTION


Określ:


- visual_style
- camera_style
- editing_style
- tone



8. SPEAKER STRATEGY


Określ:


- speaker_type

(customer,
founder,
expert,
creator,
voiceover)


- persona
- credibility_reason



9. EMOTION FLOW


Kolejność emocji:


Curiosity

Problem awareness

Hope

Trust

Confidence



10. PROOF STRATEGY


Jakie dowody powinny być wykorzystane:


- testimonial
- demo
- comparison
- numbers
- reviews



11. EXECUTION GUIDELINES


Określ:


- recommended_duration_seconds
- platforms
- formats



Zwróć wyłącznie JSON.


{
"creative_strategies":[

{

"name":"",

"objective":"",

"creative_type":"",

"recommended_format":"",


"target":{

"audience":"",

"awareness_stage":"",

"desired_action":""

},


"creative_big_idea":"",


"message_angle":"",


"hook_strategy":{

"hook_type":"",

"hook_goal":"",

"hook_direction":""

},


"story_framework":[

""

],


"creative_direction":{

"visual_style":"",

"camera_style":"",

"editing_style":"",

"tone":""

},


"speaker_strategy":{

"speaker_type":"",

"persona":"",

"credibility_reason":""

},


"emotion_flow":[

""

],


"proof_strategy":[

""

],


"execution_guidelines":{

"recommended_duration_seconds":30,

"platforms":[

""

],

"formats":[

""

]

}


}

]

}


Bez markdown.
Bez komentarzy.
Tylko JSON.
"""



USER_PROMPT_TEMPLATE = """

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

    knowledge_id:int,

    brand_marketing_id:int,

    marketing_strategy_id:int,

    offer_strategy_id:int,

    message_strategy_id:int,

    ad_strategy_id:int

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
            knowledge_id
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

            "raw_response":
            response.content

        }




    created_ids = []



    for item in result.get(
        "creative_strategies",
        []
    ):



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


            objective=item.get(
                "objective"
            ),


            creative_type=item.get(
                "creative_type"
            ),


            recommended_format=item.get(
                "recommended_format"
            ),


            target=item.get(
                "target"
            ),


            creative_big_idea=item.get(
                "creative_big_idea"
            ),


            message_angle=item.get(
                "message_angle"
            ),


            hook_strategy=item.get(
                "hook_strategy"
            ),


            story_framework=item.get(
                "story_framework",
                []
            ),


            creative_direction=item.get(
                "creative_direction"
            ),


            speaker_strategy=item.get(
                "speaker_strategy"
            ),


            emotion_flow=item.get(
                "emotion_flow",
                []
            ),


            proof_strategy=item.get(
                "proof_strategy",
                []
            ),


            execution_guidelines=item.get(
                "execution_guidelines"
            )

        )



        created = (
            creative_strategy_repository
            .create(entity)
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