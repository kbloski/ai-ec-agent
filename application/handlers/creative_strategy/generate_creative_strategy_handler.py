import json

from di.container import Container
from domain.models.ollama.llm_ollama_message import LlmOllamaMessage
from domain.enums.ollama_message_role import OllamaMessageRole
from domain.models.creative_strategy.creative_strategy import CreativeStrategy


SYSTEM_PROMPT = """
Jesteś ekspertem od Performance Creative,
Direct Response Advertising oraz Brand Storytelling.


Twoim zadaniem jest stworzenie CREATIVE STRATEGY
na podstawie pełnego kontekstu marketingowego oraz Ad Strategy.


ŹRÓDŁA:

- Knowledge Base
- Brand Strategy
- Marketing Strategy
- Offer Strategy
- Message Strategy
- Ad Strategy



CREATIVE STRATEGY NIE TWORZY:

- finalnego copy,
- scenariusza video,
- gotowych reklam.


Jej zadaniem jest rozwinięcie wybranego konceptu z Ad Strategy
w spójny kierunek kreatywny.



GENERUJ:


1. OBJECTIVE

Cel kreacji.


2. CREATIVE TYPE

Np. video, static, carousel, ugc.


3. RECOMMENDED FORMAT

Rekomendowany format reklamy.


4. TARGET

Segment odbiorcy, dla którego tworzona jest kreacja.


5. CREATIVE BIG IDEA

Główna idea kreatywna.


6. MESSAGE ANGLE

Kąt komunikacji, na którym bazuje kreacja.


7. HOOK STRATEGY

Określ:

- type
- goal
- direction


8. STORY FRAMEWORK

Struktura narracyjna reklamy (np. problem -> agitacja -> rozwiązanie).


9. CREATIVE DIRECTION

Wskazówki wizualne i stylistyczne.


10. SPEAKER STRATEGY

Kto mówi, w jakiej roli, z jakim tonem.


11. EMOTION FLOW

Sekwencja emocji w trakcie reklamy.


12. PROOF STRATEGY

Jakie dowody społeczne / dane / testimoniale są potrzebne.


13. EXECUTION GUIDELINES

Wskazówki dla zespołu produkcyjnego.



NIE GENERUJ:

- gotowego scenariusza,
- dialogów,
- grafik,
- promptów AI.



Zwróć wyłącznie JSON:


{
"creative_strategies":[

{
"name":"",
"objective":"",
"creative_type":"",
"recommended_format":"",
"target":{},
"creative_big_idea":"",
"message_angle":"",
"hook_strategy":{},
"story_framework":[],
"creative_direction":{},
"speaker_strategy":{},
"emotion_flow":[],
"proof_strategy":[],
"execution_guidelines":{}
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


    ad_strategy = (
        ad_strategy_service.get_ad_strategy_by_id(
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

            knowledge_id=knowledge_id,

            brand_marketing_id=brand_marketing_id,

            marketing_strategy_id=marketing_strategy_id,

            offer_strategy_id=offer_strategy_id,

            message_strategy_id=message_strategy_id,

            ad_strategy_id=ad_strategy_id,

            name=item.get("name"),

            objective=item.get("objective"),

            creative_type=item.get("creative_type"),

            recommended_format=item.get("recommended_format"),

            target=item.get("target"),

            creative_big_idea=item.get("creative_big_idea"),

            message_angle=item.get("message_angle"),

            hook_strategy=item.get("hook_strategy"),

            story_framework=item.get("story_framework", []),

            creative_direction=item.get("creative_direction"),

            speaker_strategy=item.get("speaker_strategy"),

            emotion_flow=item.get("emotion_flow", []),

            proof_strategy=item.get("proof_strategy", []),

            execution_guidelines=item.get("execution_guidelines"),

        )

        created = creative_strategy_repository.create(entity)

        created_ids.append(created.id)


    return [
        creative_strategy_service.get_creative_strategy_by_id(id)
        for id in created_ids
    ]
