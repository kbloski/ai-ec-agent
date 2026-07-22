import json
from random import randint
from di.container import Container

from domain.models.ollama.llm_ollama_message import LlmOllamaMessage
from domain.enums.ollama_message_role import OllamaMessageRole

from domain.models.ad_execution.ad_execution import AdExecution



SYSTEM_PROMPT = """
Jesteś ekspertem od Performance Creative,
Direct Response Advertising oraz Video Advertising.


Twoim zadaniem jest stworzenie AD EXECUTION
na podstawie pełnego kontekstu marketingowego.


ŹRÓDŁA:

- Knowledge Base
- Brand Strategy
- Marketing Strategy
- Offer Strategy
- Message Strategy
- Ad Strategy
- Creative Strategy



AD EXECUTION NIE TWORZY STRATEGII.


Jego zadaniem jest zamiana Creative Strategy
na dokładny blueprint reklamy.



GENERUJ:


1. EXECUTION


Określ:

- platform
- format
- placement
- duration_seconds
- aspect_ratio
- creative_type
- objective
- audience
- message_angle
- main_message



2. HOOK STRATEGY


Nie twórz finalnego copy.


Określ:

- type
- goal
- direction
- duration_seconds



3. STRUCTURE


Reklama powinna posiadać:


hook

problem

solution

proof

offer

cta



Każda sekcja:


{
"name":"",
"start_second":0,
"end_second":3,
"goal":"",
"emotion":""
}



4. SCENES


Każda scena:


{
"order":1,

"section":"hook",

"duration_seconds":3,

"purpose":"",

"visual":"",

"camera_direction":"",

"voiceover":"",

"dialogue":"",

"on_screen_text":"",

"emotion":""

}



5. ASSET REQUIREMENTS


Określ wymagane elementy:

- video footage
- product shots
- testimonials
- screenshots
- animations



6. PRODUCTION NOTES


Określ:

- shooting_style
- editing_style
- important_details



7. CTA


Określ:

- goal
- action_type
- placement



ZASADA CZASU:


Suma:

scenes[].duration_seconds


MUSI być dokładnie równa:

duration_seconds



NIE GENERUJ:

- grafik
- video
- promptów AI
- gotowych reklam


Zwróć tylko JSON.


FORMAT:


{
"ad_executions":[

{

"name":"",

"execution":{},

"hook_strategy":{},

"structure":[],

"scenes":[],

"asset_requirements":[],

"production_notes":{},

"cta":{}

}

]

}


Bez markdown.
Bez komentarzy.
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



CREATIVE STRATEGY:

{creative_strategy_json}



PARAMETERS:


Platform:

{platform}



Format:

{format}



Duration:

{duration_seconds}

"""




def generate_ad_execution_handler(
    knowledge_id: int,
    brand_marketing_id: int,
    marketing_strategy_id: int,
    offer_strategy_id: int,
    message_strategy_id: int,
    ad_strategy_id: int,
    creative_strategy_id: int,
    video_duration_seconds: int = 15,
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


    creative_strategy_service = (
        container.creative_strategy_service()
    )



    ad_execution_repository = (
        container.ad_execution_repository()
    )


    ad_execution_service = (
        container.ad_execution_service()
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


    creative_strategy = (
        creative_strategy_service
        .get_creative_strategy_by_id(
            id=creative_strategy_id
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
        message_strategy_json=serialize(message_strategy),
        ad_strategy_json=serialize(ad_strategy),
        creative_strategy_json=serialize( creative_strategy ),
        platform=platform,
        format=format,
        duration_seconds=video_duration_seconds
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

    for item in result.get( "ad_executions", [] ):
        scenes = item.get(
            "scenes",[]
        )

        entity = AdExecution(
            knowledge_id=knowledge_id,
            brand_marketing_id=brand_marketing_id,
            marketing_strategy_id=marketing_strategy_id,
            offer_strategy_id=offer_strategy_id,
            message_strategy_id=message_strategy_id,
            ad_strategy_id=ad_strategy_id,
            creative_strategy_id=creative_strategy_id,
            name=f"{randint(0, 1000)}{item.get('name')}",
            execution=item.get("execution"),
            hook_strategy=item.get("hook_strategy"),
            structure=item.get("structure", []),
            scenes=scenes,
            asset_requirements=item.get("asset_requirements", []),
            production_notes=item.get("production_notes"),
            cta=item.get("cta")
        )

        created = (
            ad_execution_repository .create( entity )
        )

        created_ids.append(
            created.id
        )

    return [
        ad_execution_service.get_ad_execution_by_id( id )
        for id in created_ids
    ]