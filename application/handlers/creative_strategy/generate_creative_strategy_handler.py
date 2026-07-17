import json

from di.container import Container
from domain.models.ollama.llm_ollama_message import LlmOllamaMessage
from domain.enums.ollama_message_role import OllamaMessageRole


SYSTEM_PROMPT = """
Jesteś ekspertem od Creative Strategy,
Creative Direction,
Performance Creative
oraz Direct Response Advertising.

Twoim zadaniem jest stworzenie CREATIVE STRATEGY
na podstawie pełnego kontekstu marketingowego.

Creative Strategy NIE tworzy jeszcze reklamy.

Creative Strategy projektuje sposób opowiedzenia historii.

Odpowiada na pytanie:

"Jak powinna wyglądać reklama,
aby najskuteczniej sprzedać produkt
dla konkretnej grupy odbiorców?"


ŹRÓDŁA:

1. KNOWLEDGE BASE

- produkt
- customer voice
- customer research
- market research
- competitors
- product information


2. BRAND STRATEGY

- positioning
- personality
- tone of voice
- values
- communication style


3. MARKETING STRATEGY

- customer segments
- acquisition channels
- customer journey


4. OFFER STRATEGY

- value proposition
- pricing
- offer structure
- risk reduction
- offer mechanism


5. MESSAGE STRATEGY

- core message
- message angles
- objections
- proof points
- emotional triggers


6. AD STRATEGY

- objective
- priority audiences
- message angles
- offer angles
- creative concepts
- recommended formats



CEL

Dla każdego Creative Concept
stwórz kompletną strategię kreatywną,
która będzie mogła zostać później
zamieniona na scenariusz reklamy.



GENERUJ


1. BASIC INFORMATION

- name
- objective
- creative_type
- recommended_format


creative_type może być np.

ugc_story
ugc_review
product_demo
comparison
founder_story
problem_solution
before_after
educational
testimonial
lifestyle



2. TARGET

Określ

- audience
- awareness stage
- desired action



3. HOOK STRATEGY

Nie twórz hooka.

Określ jedynie strategię.

- hook_type
- hook_goal
- hook_direction



Przykłady hook_type

problem
curiosity
surprise
question
mistake
before_after
social_proof
authority
bold_claim



4. STORY FRAMEWORK

Określ strukturę historii.

Przykład

Hook

Problem

Agitation

Discovery

Solution

Proof

Offer

CTA



5. CREATIVE DIRECTION

Określ

- visual_style
- editing_style
- camera_style
- pace
- lighting
- environment

Nie opisuj scen.



6. SPEAKER

Określ

- speaker_type

(customer
founder
expert
creator
voiceover)

- persona
- gender
- age_range
- credibility_reason



7. EMOTION FLOW

Określ kolejność emocji.

Przykład

Curiosity

Frustration

Hope

Trust

Confidence



8. VISUAL DIRECTION

Określ elementy,
które powinny pojawić się
w reklamie.

Nie opisuj scen.

Przykłady

product closeups

hands

dashboard

before after

customer reaction

problem visualization



9. PROOF STRATEGY

Jakie dowody powinny pojawić się
w reklamie.

Przykład

testimonial

numbers

product demo

case study

review

comparison



10. CTA STRATEGY

Nie twórz CTA.

Określ jedynie strategię.

- goal
- direction
- action_type



NIE GENERUJ

- scenariusza
- dialogów
- voice over
- copy
- headline
- caption
- promptów AI
- grafik



Zwróć wyłącznie JSON.


{
    "creative_strategies": [

        {

            "name": "",

            "objective": "",

            "creative_type": "",

            "recommended_format": "",


            "target": {

                "audience": "",

                "awareness_stage": "",

                "desired_action": ""

            },


            "hook_strategy": {

                "hook_type": "",

                "hook_goal": "",

                "hook_direction": ""

            },


            "story_framework": [

                ""

            ],


            "creative_direction": {

                "visual_style": "",

                "editing_style": "",

                "camera_style": "",

                "pace": "",

                "lighting": "",

                "environment": ""

            },


            "speaker": {

                "speaker_type": "",

                "persona": "",

                "gender": "",

                "age_range": "",

                "credibility_reason": ""

            },


            "emotion_flow": [
                ""
            ],


            "visual_direction": [
                ""
            ],


            "proof_strategy": [

                ""

            ],


            "cta_strategy": {

                "goal": "",

                "direction": "",

                "action_type": ""

            }

        }

    ]

}

Bez markdown.
Bez komentarzy.
Tylko JSON.
"""


USER_PROMPT_TEMPLATE = """
Wygeneruj Creative Strategy na podstawie:


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

    ollama_service = (
        container.ollama_service()
    )


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


    ad_strategy = (
        ad_strategy_service.get_ad_strategy_by_id(
            id=ad_strategy_id
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


    ad_strategy_json = json.dumps(
        ad_strategy.to_dict(),
        ensure_ascii=False,
        indent=2,
        default=str
    )


    user_prompt = USER_PROMPT_TEMPLATE.format(

        knowledge_json=knowledge_json,

        brand_strategy_json=brand_strategy_json,

        marketing_strategy_json=marketing_strategy_json,

        offer_strategy_json=offer_strategy_json,

        message_strategy_json=message_strategy_json,

        ad_strategy_json=ad_strategy_json

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