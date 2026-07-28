import json

from di.container import Container
from domain.models.ollama.llm_ollama_message import LlmOllamaMessage
from domain.enums.ollama_message_role import OllamaMessageRole
from domain.models.creative_strategy.creative_strategy import CreativeStrategy


SYSTEM_PROMPT = """
You are an expert in Performance Creative,
Direct Response Advertising, and Brand Strategy.

Your task is to create a CREATIVE STRATEGY
based on the marketing context and Ad Strategy.

CREATIVE STRATEGY defines:
- why this creative should exist,
- what communication direction it should follow,
- who it is for,
- what message it should deliver.

It does NOT define production details.

DO NOT CREATE:
- video scripts,
- dialogues,
- scenes,
- visual directions,
- creators,
- camera instructions,
- finished advertisements.


GENERATE:


1. OBJECTIVE

Define the main business goal of the creative.


2. CREATIVE TYPE

Define the recommended creative category.

Examples:
- UGC,
- testimonial,
- product demonstration,
- educational,
- comparison,
- lifestyle.


3. RECOMMENDED FORMAT

Define the recommended advertising format.

Examples:
- short form video,
- static image,
- carousel.


4. TARGET

Define the audience segment:

Include:
- demographics,
- awareness level,
- motivations,
- pain points.


5. CREATIVE BIG IDEA

Define the central creative concept.

Important:
- Describe the strategic direction.
- Do not write headlines.
- Do not write advertising copy.


6. MESSAGE ANGLE

Define the main communication angle.

Examples:
- problem awareness,
- transformation,
- trust,
- education,
- proof.


7. HOOK STRATEGY

Define:

- hook type,
- attention goal,
- communication direction.

Do not generate actual hooks.


8. EMOTION FLOW

Define the emotional journey.

Example:

[
    "curiosity",
    "recognition",
    "trust",
    "desire"
]


9. PROOF STRATEGY

Define what evidence should support the message.

Examples:
- testimonials,
- demonstrations,
- customer results,
- product evidence,
- social proof.



Return only valid JSON:

{
    "creative_strategies": [
        {
            "name": "",

            "objective": "",

            "creative_type": "",

            "recommended_format": "",

            "target": {},

            "creative_big_idea": "",

            "message_angle": "",

            "hook_strategy": {
                "type": "",
                "goal": "",
                "direction": ""
            },

            "emotion_flow": [],

            "proof_strategy": []
        }
    ]
}


STRICT JSON RULES:
- Return only valid JSON.
"""


USER_PROMPT_TEMPLATE = """
Generate a Creative Strategy based on the following data:


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
    ad_strategy_id: int
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

    ad_strategy_service = (
        container.ad_strategy_service()
    )

    creative_strategy_repository = container.creative_strategy_repository()
    creative_strategy_service = container.creative_strategy_service()

    ollama_service = container.ollama_service()



    ad_strategy = (
        ad_strategy_service.get_ad_strategy_by_id(
            id=ad_strategy_id
        )
    )


    message_strategy = (
        message_strategy_service.get_message_strategy_by_id(
            id=ad_strategy.message_strategy_id
        )
    )


    offer_strategy = (
        offer_strategy_service.get_offer_strategy_by_id(
            id=message_strategy.offer_strategy_id
        )
    )


    marketing_strategy = (
        marketing_strategy_service.get_marketing_strategy_by_id(
            id=offer_strategy.marketing_strategy_id
        )
    )


    brand_strategy = (
        brand_marketing_service.get_brand_marketing_by_id(
            id=marketing_strategy.brand_marketing_id
        )
    )


    knowledge = (
        knowledge_service.get_knowledge_details_by_id(
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

        ad_strategy_json=serialize(ad_strategy)

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



    created_ids = []


    for item in result.get("creative_strategies", []):

        entity = CreativeStrategy(

            ad_strategy_id=ad_strategy_id,

            name=item.get("name"),

            objective=item.get("objective"),

            creative_type=item.get("creative_type"),

            recommended_format=item.get("recommended_format"),

            target=item.get("target"),

            creative_big_idea=item.get("creative_big_idea"),

            message_angle=item.get("message_angle"),

            hook_strategy=item.get("hook_strategy"),

            emotion_flow=item.get("emotion_flow", []),

            proof_strategy=item.get("proof_strategy", [])

        )

        created = creative_strategy_repository.create(entity)

        created_ids.append(created.id)


    return [
        creative_strategy_service.get_creative_strategy_by_id(id)
        for id in created_ids
    ]
