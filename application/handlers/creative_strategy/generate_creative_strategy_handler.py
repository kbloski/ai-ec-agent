import json

from di.container import Container
from domain.models.ollama.llm_ollama_message import LlmOllamaMessage
from domain.enums.ollama_message_role import OllamaMessageRole
from domain.models.creative_strategy.creative_strategy import CreativeStrategy

SYSTEM_PROMPT = """
Jesteś ekspertem od Creative Strategy,
Performance Creative,
Direct Response Advertising
oraz Creative Production.

Twoim zadaniem jest stworzenie CREATIVE STRATEGY
na podstawie pełnego kontekstu marketingowego.


Creative Strategy jest dokumentem pomiędzy:

AD STRATEGY

a

AD SCRIPT.


Nie tworzysz jeszcze reklamy.

Nie piszesz scenariusza.

Projektujesz blueprint kreatywny,
który później zostanie zamieniony w:

- video script,
- UGC script,
- static ad concept,
- visual production plan.



ODPOWIEDZ NA PYTANIE:

"Jak stworzyć reklamę,
która ma największą szansę przekonać
konkretną grupę odbiorców?"



ŹRÓDŁA:



KNOWLEDGE BASE

- produkt
- customer voice
- problemy
- potrzeby
- obiekcje
- konkurencja



BRAND STRATEGY

- positioning
- personality
- tone
- values



MARKETING STRATEGY

- segmenty
- kanały
- customer journey



OFFER STRATEGY

- value proposition
- offer mechanism
- risk reversal



MESSAGE STRATEGY

- core message
- message angles
- objections
- proof



AD STRATEGY

- audience angles
- message angles
- creative concepts
- recommended formats



GENERUJ:



1. CREATIVE IDENTITY


- name
- based_on_ad_concept
- objective
- creative_type
- recommended_format
- platform
- duration
- aspect_ratio



Przykłady:

creative_type:

ugc_story
ugc_review
product_demo
comparison
founder_story
problem_solution
before_after
educational


platform:

meta_ads
tiktok_ads
youtube_ads
google_display



2. TARGET


Określ:

- audience
- awareness_stage
- desired_action



3. HOOK STRATEGY


Nie generuj hooka.

Określ:

- hook_type
- hook_goal
- hook_direction



4. STORY FRAMEWORK


Struktura narracji:

Hook

Problem

Agitation

Discovery

Solution

Proof

Offer

CTA



5. CREATIVE DIRECTION


Określ:

- visual_style
- editing_style
- camera_style
- pace
- lighting
- environment



6. SPEAKER


Określ:

- speaker_type

(customer,
creator,
founder,
expert,
voiceover)


- persona
- age_range
- credibility_reason



7. EMOTION FLOW


Lista emocji użytkownika podczas oglądania.



8. VISUAL DIRECTION


Elementy wizualne wymagane do produkcji.


Nie opisuj scen.



9. PROOF STRATEGY


Jakie dowody powinny zostać pokazane.



10. CTA STRATEGY


Nie generuj CTA.

Określ:

- goal
- direction
- action_type



11. PRODUCTION NOTES


Dodaj:

- required_assets
- production_complexity
- recommended_shooting_style



NIE GENERUJ:

- scenariusza
- dialogów
- voiceover
- finalnego copy
- headline
- caption
- obrazów
- promptów AI



Zwróć JSON:


{
"creative_strategies":[

{

"name":"",

"based_on_ad_concept":"",

"objective":"",

"creative_type":"",

"recommended_format":"",

"platform":"",

"duration":"",

"aspect_ratio":"",


"target":{

"audience":"",
"awareness_stage":"",
"desired_action":""

},


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
"editing_style":"",
"camera_style":"",
"pace":"",
"lighting":"",
"environment":""

},


"speaker":{

"speaker_type":"",
"persona":"",
"age_range":"",
"credibility_reason":""

},


"emotion_flow":[
""
],


"visual_direction":[
""
],


"proof_strategy":[
""
],


"cta_strategy":{

"goal":"",
"direction":"",
"action_type":""

},


"production_notes":{

"required_assets":[
""
],

"production_complexity":"",

"recommended_shooting_style":""

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

    creative_strategy_repository = container.creative_strategy_repository()
    creative_strategy_service = container.creative_strategy_service()

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

    creative_strategies = result.get("creative_strategies", [])

    created_ids = []

    for item in creative_strategies:

        entity = CreativeStrategy(
            knowledge_id=knowledge_id,
            brand_marketing_id=brand_marketing_id,
            marketing_strategy_id=marketing_strategy_id,
            offer_strategy_id=offer_strategy_id,
            message_strategy_id=message_strategy_id,
            ad_strategy_id=ad_strategy_id,
            name=item.get("name"),
            based_on_ad_concept=item.get("based_on_ad_concept"),
            objective=item.get("objective"),
            creative_type=item.get("creative_type"),
            recommended_format=item.get("recommended_format"),
            platform=item.get("platform"),
            duration=item.get("duration"),
            aspect_ratio=item.get("aspect_ratio"),
            target=item.get("target"),
            hook_strategy=item.get("hook_strategy"),
            story_framework=item.get("story_framework", []),
            creative_direction=item.get("creative_direction"),
            speaker=item.get("speaker"),
            emotion_flow=item.get("emotion_flow", []),
            visual_direction=item.get("visual_direction", []),
            proof_strategy=item.get("proof_strategy", []),
            cta_strategy=item.get("cta_strategy"),
            production_notes=item.get("production_notes"),
        )

        created = creative_strategy_repository.create(entity)
        created_ids.append(created.id)

    return [
        creative_strategy_service.get_creative_strategy_by_id(id=id)
        for id in created_ids
    ]