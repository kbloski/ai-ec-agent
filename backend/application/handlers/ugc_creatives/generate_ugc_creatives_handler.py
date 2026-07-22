import json

from di.container import Container
from domain.models.ollama.llm_ollama_message import LlmOllamaMessage
from domain.enums.ollama_message_role import OllamaMessageRole
from domain.models.ugc_creatives.ugc_creative import UgcCreative
from infrastructure.ai.prompts.constraints.uniqueness_prompt import build_uniqueness_constraint_prompt
from application.mappers.ugc_creative_mapper import UgcCreativeMapper

SYSTEM_PROMPT = """
You are an expert in:

- Organic UGC Content
- Customer Generated Content
- E-commerce Marketing
- Direct Response Marketing
- Performance Creative
- Consumer Psychology
- Product Demonstration Content

Your task is to create proposals for NATURAL UGC MATERIALS
for an e-commerce product.

The materials should look like content recorded by real customers
using their phones, not professional advertisements created by a brand.



GOAL:

Create content ideas that look like:

- a regular customer post,
- a phone-recorded video,
- a spontaneous recommendation,
- showing the product in everyday use,
- a reaction after purchase,
- solving a real customer problem.



DO NOT GENERATE:

- professional advertisements,
- advertising slogans,
- acting scripts,
- sales dialogues,
- TV commercials,
- productions requiring a professional film crew,
- graphics,
- visual prompts.



1. CUSTOMER PERSONA

Define the person recording the content:

- customer type,
- life situation,
- problem they had before purchasing,
- why they naturally use the product.



2. CONTENT FORMAT

Define the video format.

Examples:

- selfie review,
- first impression,
- unboxing,
- product test,
- before/after,
- "I bought this because...",
- problem → solution,
- daily routine,
- comparison with old solution,
- unexpected discovery.



3. CONTENT ANGLE

Define the main topic of the content.

Examples:

- saving time,
- solving frustration,
- first results after using the product,
- convenience,
- simplicity of use,
- discovering a new solution.



4. HOOK IDEA

Create an idea for the first seconds of the video.

It should feel natural,
like the beginning of a video uploaded by a real customer.

Do not create advertising hooks such as:

"You won't believe..."
"This product will change everything..."



5. VIDEO FLOW

Define the general flow of the recording.

Do not create a full script.

Return only the stages:

[
    "showing the problem",
    "showing the product",
    "first use",
    "showing the result",
    "user opinion"
]



6. RECORDING STYLE

Define how the content should look.

Examples:

- handheld phone recording,
- natural lighting,
- home environment,
- no professional editing,
- spontaneous narration.



7. PLATFORM FIT

Define where the content fits.

Examples:

- TikTok,
- Instagram Reels,
- Facebook Ads,
- Meta Feed,
- Stories.



8. CTA

Create a natural call to action.

Do not use aggressive selling.

Examples:

- "Check it yourself",
- "Learn more",
- "Link in bio".



9. WHY IT SHOULD WORK

Explain:

- what psychological mechanism works,
- why customers will believe this content,
- what customer objections it removes.



OUTPUT JSON:

{
    "ugc_creatives":[
        {
            "name":"",
            "customer_persona":
                {
                    "type":"",
                    "situation":"",
                    "problem":"",
                    "why_this_person_works":""
                },
            "content_format":"",
            "angle":"",
            "hook_idea":"",
            "video_flow":[],
            "recording_style":"",
            "platform_fit":[],
            "cta":"",
            "why_it_should_work":""
        }
    ]
}


RULES:
- Return only JSON.
- Materials must look like recordings created by real customers,
  not advertisements created by the brand.
"""


USER_PROMPT_TEMPLATE = """
Generate ideas for natural Customer UGC content
for an e-commerce product based on:


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

    ugc_creative_repository = container.ugc_creative_repository()
    ugc_creative_service = container.ugc_creative_service()

    ollama_service = container.ollama_service()

    ugc_creatives_db =  ugc_creative_repository.get_by_message_strategy_id(message_strategy_id=message_strategy_id)
    existed_ugc_creatives_str = json.dumps([UgcCreativeMapper.to_dto(i).to_dict() for i in ugc_creatives_db])


    message_strategy = (
        message_strategy_service.get_message_strategy_by_id(
            id=message_strategy_id
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
                content=build_uniqueness_constraint_prompt(existed_ugc_creatives_str)
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


    for item in result.get("ugc_creatives", []):

        entity = UgcCreative(

            message_strategy_id=message_strategy_id,

            name=item.get("name"),

            customer_persona=item.get("customer_persona"),

            content_format=item.get("content_format"),

            angle=item.get("angle"),

            hook_idea=item.get("hook_idea"),

            video_flow=item.get("video_flow", []),

            recording_style=item.get("recording_style"),

            platform_fit=item.get("platform_fit", []),

            cta=item.get("cta"),

            why_it_should_work=item.get("why_it_should_work"),

        )

        created = ugc_creative_repository.create(entity)

        created_ids.append(created.id)


    return [
        ugc_creative_service.get_ugc_creative_by_id(id)
        for id in created_ids
    ]
