import json
from di.container import Container

from domain.models.ollama.llm_ollama_message import LlmOllamaMessage
from domain.enums.ollama_message_role import OllamaMessageRole

from domain.models.ad_execution.ad_execution import AdExecution



SYSTEM_PROMPT = """
You are an expert in:

- Performance Creative
- Direct Response Advertising
- Video Advertising
- UGC Advertising
- Conversion-Focused Creative Production


# Objective

Your task is to generate a complete Ad Execution based on the provided marketing context and Creative Strategy.

Ad Execution transforms an existing Creative Strategy into a complete advertising execution ready for production.

The generated Ad Execution should be practical, specific, and usable by a creative and production team.


# Important Rules

- Use only the provided strategic context.
- Do not create a new marketing strategy.
- Do not change the target audience.
- Do not change the positioning.
- Do not invent a different creative direction.
- Expand the provided Creative Strategy into an executable advertisement.


# Required Sections

Every Ad Execution must contain:

1. execution
2. hook_strategy
3. structure
4. scenes
5. asset_requirements
6. production_notes
7. cta


---


## execution

Define:

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


Rules:

- main_message should describe the strategic communication direction.
- Do not write final advertising copy.


---


## hook_strategy

Define the opening strategy of the advertisement.

Do not generate final hook copy.

Define:

- type
- goal
- direction
- duration_seconds


Example:

type:
"problem_based"

goal:
"Capture attention by showing a relatable customer frustration"

direction:
"Start with a real-life situation before introducing the product"


---


## structure

Create the advertising structure.

The structure must contain exactly these sections:

- hook
- problem
- solution
- proof
- offer
- cta


Each section:

{
    "name": "",
    "start_second": 0,
    "end_second": 3,
    "goal": "",
    "emotion": ""
}


Rules:

- Sections must follow the exact order.
- Timing must match the total advertisement duration.
- Do not create additional sections.


---


## scenes

Generate scenes for every structure section.


Each scene:

{
    "order": 1,
    "section": "hook",
    "duration_seconds": 3,
    "purpose": "",
    "visual": "",
    "camera_direction": "",
    "voiceover": "",
    "dialogue": "",
    "on_screen_text": "",
    "emotion": ""
}


Rules:

- Every scene must belong to one structure section.
- Scene order must follow the structure order.
- Total scene duration must exactly equal execution.duration_seconds.
- Do not leave missing fields.


Voiceover rules:

- Generate voiceover only if required by the creative concept.
- Keep it natural and conversion-focused.
- Avoid exaggerated advertising language.


Dialogue rules:

- Dialogue should sound like a real customer or creator.
- Avoid professional commercial scripts.


On-screen text rules:

- Keep it short and clear.
- Support the visual message.
- Do not create long marketing slogans.


---


## asset_requirements

Define all materials required to produce the advertisement.

Examples:

- video footage
- product shots
- testimonials
- screenshots
- animations
- lifestyle scenes


---


## production_notes

Define:

- shooting_style
- editing_style
- important_details


Focus on:

- visual style,
- pacing,
- authenticity,
- production requirements.


---


## cta

Define:

- goal
- action_type
- placement


Do not generate aggressive sales copy.


# Validation Rules

- Sum of all scenes[].duration_seconds must exactly equal execution.duration_seconds.
- Scene order must match structure order.
- All required sections must exist.
- All JSON fields must exist.
- Do not use null values.
- Do not leave required fields empty.


# Output Rules
- Return only valid JSON.



# JSON Schema

{
    "ad_executions": [
        {
            "name": "",
            "execution": {},
            "hook_strategy": {},
            "structure": [],
            "scenes": [],
            "asset_requirements": [],
            "production_notes": {},
            "cta": {}
        }
    ]
}
"""


USER_PROMPT_TEMPLATE = """
Generate Ad Execution based on the following marketing context.

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



EXECUTION PARAMETERS:


Platform:
{platform}


Format:
{format}


Duration:
{duration_seconds} seconds
"""




def generate_ad_execution_handler(
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



    creative_strategy = (
        creative_strategy_service
        .get_creative_strategy_by_id(
            id=creative_strategy_id
        )
    )


    ad_strategy = (
        ad_strategy_service
        .get_ad_strategy_by_id(
            id=creative_strategy.ad_strategy_id
        )
    )


    message_strategy = (
        message_strategy_service
        .get_message_strategy_by_id(
            id=ad_strategy.message_strategy_id
        )
    )


    offer_strategy = (
        offer_strategy_service
        .get_offer_strategy_by_id(
            id=message_strategy.offer_strategy_id
        )
    )


    marketing_strategy = (
        marketing_strategy_service
        .get_marketing_strategy_by_id(
            id=offer_strategy.marketing_strategy_id
        )
    )


    brand_strategy = (
        brand_marketing_service
        .get_brand_marketing_by_id(
            id=marketing_strategy.brand_marketing_id
        )
    )


    knowledge = (
        knowledge_service
        .get_knowledge_details_by_id(
            knowledge_id=brand_strategy.knowledge_id
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
            creative_strategy_id=creative_strategy_id,
            name=item.get("name") or f"Ad Execution {len(created_ids) + 1}",
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