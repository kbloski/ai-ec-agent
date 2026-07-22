import json

from di.container import Container

from domain.models.ollama.llm_ollama_message import (
    LlmOllamaMessage
)

from domain.enums.ollama_message_role import (
    OllamaMessageRole
)

from domain.models.video_creative_execution.video_creative_execution import (
    VideoCreativeExecution
)


SYSTEM_PROMPT = """
You are an expert Performance Creative Director specializing in:

- Direct Response Advertising
- Meta Ads Creative Production
- UGC Advertising
- Conversion-Focused Video Ads
- Short Form Video Storytelling
- Creative Testing


# Objective

Your task is to transform an existing Ad Execution into a complete video production brief.

The output will be used by:
- video creators,
- UGC creators,
- editors,
- designers,
- advertising teams.

Generate a practical production-ready video concept.

Do not create a new strategy.
Do not change positioning.
Do not change audience.
Expand only the existing Ad Execution.


# Core Principles

The video must be designed for conversion.

Every decision should answer:

- Why will someone stop scrolling?
- Why will someone keep watching?
- Why will someone trust the product?
- Why will someone take action?


# Required Output


## hook_strategy

Define the first seconds of the video.

The hook must describe the attention mechanism, not final copy.

Include:

{
"type":"",
"goal":"",
"psychological_trigger":"",
"visual_direction":"",
"duration_seconds":0
}


Possible hook types:

- problem_based
- curiosity
- pattern_interrupt
- emotional
- demonstration
- social_proof
- transformation


Examples:

Good:

{
"type":"pattern_interrupt",
"goal":"Stop scrolling by showing an unexpected everyday situation",
"psychological_trigger":"Curiosity gap",
"visual_direction":"Open with a close-up action before explaining the product",
"duration_seconds":3
}


Bad:

{
"type":"attention grabbing",
"goal":"grab attention"
}


---


## structure


Create the complete video structure.

Required sections:

1. hook
2. problem
3. solution
4. proof
5. offer
6. cta


Each section:

{
"name":"",
"start_second":0,
"end_second":0,
"goal":"",
"emotion":"",
"viewer_question":""
}


The viewer_question explains what the viewer should think at this moment.


Example:

{
"name":"problem",
"goal":"Show the frustration before introducing the solution",
"emotion":"recognition",
"viewer_question":"Do I have this problem?"
}


Rules:

- Follow exact order.
- Match total duration.
- No additional sections.


---


## scenes


Create scenes matching every structure section.


Each scene:

{
"order":1,
"section":"",
"duration_seconds":0,
"purpose":"",
"visual":"",
"camera_direction":"",
"voiceover":"",
"dialogue":"",
"on_screen_text":"",
"emotion":"",
"editing_notes":""
}


Rules:

Visuals must be specific.

Bad:

"Person using product"


Good:

"Close-up shot of hands opening the glass jar, removing a colored card, natural morning light, home environment"


Camera direction should describe:

- shot type
- movement
- framing


Dialogue rules:

- Natural human speech.
- Avoid advertising language.
- Sound like a real customer or creator.


Voiceover rules:

- Use only when it improves storytelling.
- Keep conversational.


On-screen text:

- Short.
- Supports the visual.
- Maximum 5-8 words.


---


## asset_requirements


List every asset needed:

Examples:

- product shots
- lifestyle footage
- UGC footage
- screenshots
- animations
- testimonials
- before/after shots


Make them production specific.


---


## production_notes


Define:

{
"shooting_style":"",
"editing_style":"",
"pacing":"",
"visual_style":"",
"important_details":[]
}


Focus on:

- authenticity,
- retention,
- conversion,
- platform requirements.


---


## cta


Define:

{
"goal":"",
"action_type":"",
"placement":"",
"visual_direction":""
}


Do not write aggressive sales copy.


# Validation

Before returning:

- Scene durations must equal total video duration.
- Every section must have scenes.
- No empty fields.
- No null values.
- Return JSON only.


# Output Schema

{
"hook_strategy":{},
"structure":[],
"scenes":[],
"asset_requirements":[],
"production_notes":{},
"cta":{}
}

"""

USER_PROMPT = """
Generate video creative execution.

AD EXECUTION:

{ad_execution}


CREATIVE STRATEGY:

{creative_strategy}


BRAND STRATEGY:

{brand_strategy}


MARKETING STRATEGY:

{marketing_strategy}


OFFER STRATEGY:

{offer_strategy}


MESSAGE STRATEGY:

{message_strategy}


AD STRATEGY:

{ad_strategy}


Duration:

{duration_seconds} seconds
"""


def generate_video_creative_execution_handler(
    ad_execution_id: int,
    duration_seconds: int = 15
):

    container = Container()


    ad_execution_service = (
        container.ad_execution_service()
    )

    video_creative_execution_service = (
        container.video_creative_execution_service()
    )


    ollama_service = (
        container.ollama_service()
    )


    creative_strategy_service = (
        container.creative_strategy_service()
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


    ad_execution = (
        ad_execution_service
        .get_ad_execution_by_id(
            ad_execution_id
        )
    )


    creative_strategy = (
        creative_strategy_service
        .get_creative_strategy_by_id(
            ad_execution.creative_strategy_id
        )
    )


    ad_strategy = (
        ad_strategy_service
        .get_ad_strategy_by_id(
            creative_strategy.ad_strategy_id
        )
    )


    message_strategy = (
        message_strategy_service
        .get_message_strategy_by_id(
            ad_strategy.message_strategy_id
        )
    )


    offer_strategy = (
        offer_strategy_service
        .get_offer_strategy_by_id(
            message_strategy.offer_strategy_id
        )
    )


    marketing_strategy = (
        marketing_strategy_service
        .get_marketing_strategy_by_id(
            offer_strategy.marketing_strategy_id
        )
    )


    brand_strategy = (
        brand_marketing_service
        .get_brand_marketing_by_id(
            marketing_strategy.brand_marketing_id
        )
    )


    def serialize(obj):

        return json.dumps(
            obj.to_dict(),
            ensure_ascii=False,
            indent=2,
            default=str
        )


    prompt = USER_PROMPT.format(

        ad_execution=serialize(
            ad_execution
        ),

        creative_strategy=serialize(
            creative_strategy
        ),

        brand_strategy=serialize(
            brand_strategy
        ),

        marketing_strategy=serialize(
            marketing_strategy
        ),

        offer_strategy=serialize(
            offer_strategy
        ),

        message_strategy=serialize(
            message_strategy
        ),

        ad_strategy=serialize(
            ad_strategy
        ),

        duration_seconds=duration_seconds
    )


    response = ollama_service.chat_llm(

        messages=[

            LlmOllamaMessage(
                role=OllamaMessageRole.SYSTEM,
                content=SYSTEM_PROMPT
            ),


            LlmOllamaMessage(
                role=OllamaMessageRole.USER,
                content=prompt
            )

        ]

    )


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


    entity = VideoCreativeExecution(

        ad_execution_id=ad_execution_id,

        duration_seconds=duration_seconds,

        hook_strategy=result.get(
            "hook_strategy"
        ),

        structure=result.get(
            "structure",
            []
        ),

        scenes=result.get(
            "scenes",
            []
        ),

        asset_requirements=result.get(
            "asset_requirements",
            []
        ),

        production_notes=result.get(
            "production_notes"
        ),

        cta=result.get(
            "cta"
        )

    )


    return video_creative_execution_service.create_video_creative_execution(entity)