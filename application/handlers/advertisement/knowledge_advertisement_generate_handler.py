import json
import re

from di.container import Container
from domain.models.models import (
    LlmOllamaMessage, Advertisement, Scene, AdvertisementScene, AdvertisementObjection
)
from domain.enums.enums import (
    OllamaMessageRole
)



SYSTEM_PROMPT = """

Jesteś ekspertem od performance marketingu,
direct response copywritingu oraz tworzenia reklam
sprzedażowych dla platform takich jak:

- Meta Ads
- TikTok Ads
- Facebook Ads
- Instagram Ads


Twoim zadaniem jest wygenerowanie gotowych kreacji reklamowych,
które mogą zostać bezpośrednio użyte do testów reklamowych.


ZASADY STRATEGICZNE:

- Klient nie kupuje produktu.
- Klient kupuje efekt, zmianę i rozwiązanie problemu.

Każda reklama musi:

- identyfikować konkretny problem klienta,
- pokazywać emocjonalny powód zakupu,
- prezentować produkt jako rozwiązanie,
- posiadać mocny hook,
- posiadać jasne CTA.


NIE TWÓRZ:

- ogólnych reklam,
- pustych sloganów,
- marketingowego bełkotu,
- fałszywych opinii,
- fałszywych statystyk,
- wymyślonych certyfikatów.


Jeżeli produkt nie posiada danych typu:

- opinie,
- liczby,
- badania,
- wyniki,

pole proof pozostaw puste.


FORMATY REKLAM:

Wykorzystuj różne frameworki:

- Before / After
- Problem Solution
- Product Demo
- Testimonial
- Feature Benefit
- US vs THEM
- Bold Claim
- Offer Sale
- Native
- Negative Hook
- What's Inside
- Comparison
- Founder Story


KAŻDA REKLAMA MUSI BYĆ INNYM EKSPERYMENTEM:

Musi posiadać:

- inny framework,
- inny angle,
- inny trigger psychologiczny,
- inny hook,
- inną hipotezę marketingową.


HOOK:

Pierwsze 3 sekundy są najważniejsze.

Hook musi:

- zatrzymać scrollowanie,
- dotyczyć klienta,
- wywołać emocję,
- być prosty,
- być konkretny.


COPY:

Używaj:

- prostego języka,
- krótkich zdań,
- języka klienta,
- korzyści zamiast cech.


LICZBY:

Wszystkie pola liczbowe MUSZĄ być integer.

Poprawnie:

{
"duration_seconds":15,
"duration":3,
"hook":8
}


Niepoprawnie:

{
"duration_seconds":"15 sekund",
"duration":"0-3s",
"hook":"8/10"
}



ODPOWIEDŹ:

Zwróć wyłącznie poprawny JSON.

Nie dodawaj:

- markdown,
- ```json,
- komentarzy,
- opisów przed JSON.

"""


USER_PROMPT_TEMPLATE = """

Na podstawie danych produktu wygeneruj dokładnie:

{count}

różnych reklam.


DANE PRODUKTU:

{product_json}

Zwróć dokładnie strukturę:

{{
"advertisements":[
    {{
        "name":"",
        "strategy":{{
            "framework":"",
            "angle":"",
            "psychology_trigger":"",
            "awareness_stage":"",
            "hypothesis":""

        }},
        "creative":{{
            "platform":"",
            "format":"",
            "duration_seconds":15,
            "aspect_ratio":"9:16",
            "hook":{{
                "text":"",
                "type":"",
                "visual":"",
                "duration":3

            }},
            "problem":"",
            "solution":"",
            "proof":{{
                "type":"",
                "content":""

            }},
            "scenes":[
                {{
                    "order":1,
                    "type" : "",
                    "description":"",
                    "duration_seconds":3
                }}
            ],
            "voiceover":"",
            "visual_direction":[
                ""
            ],
            "text_overlays":[
                ""
            ],
            "cta":{{
                "text":"",
                "type":"",
                "urgency":""
            }}
        }},
        "target_audience":{{
            "name":"",
            "pain_points":[
                ""
            ],
            "motivations":[
                ""
            ],
            "buying_triggers":[
                ""
            ]
        }},
        "objections_handled":[
            {{
                "objection":"",
                "answer":""
            }}
        ],
        "score":{{
            "hook":0,
            "emotion":0,
            "clarity":0,
            "purchase_intent":0,
            "overall":0
        }}
    }}
]
}}


DODATKOWE ZASADY:

1.Wygeneruj dokładnie {count} elementów.

2.Każda reklama musi mieć:
- inny framework,
- inny hook,
- inną grupę odbiorców,
- inny problem,
- inną hipotezę testową.

3. SCRIPT:
Script jest tablicą scen filmu.
Każda scena posiada:
- order,
- description,
- duration_seconds.

4.PROOF:
Nigdy nie wymyślaj dowodów.
Jeżeli brak danych:
"type":"",
"content":""

5.CTA:
CTA musi mówić użytkownikowi co zrobić.

Przykłady:
- Zamów teraz
- Sprawdź ofertę
- Zobacz jak działa
- Poznaj szczegóły

6.SCORE:
Skala 1-10.
Każda wartość musi być integer.
"""


def knowledge_advertisement_generate_handler(
    knowledge_id: int,
    count: int
):

    if count <= 0:
        raise ValueError(
            "count musi być większe od 0"
        )


    container = Container()


    knowledge_service = container.knowledge_service()
    

    ollama_service = container.ollama_service()

    advertisements_repository = container.advertisements_repository()
    scenes_repository = container.scenes_repository()
    advertisement_scenes_repository = container.advertisement_scenes_repository()
    advertisement_objections_repository = container.advertisement_objections_repository()
    advertisement_service = container.advertisement_service()

    knowledge_details =  knowledge_service .get_knowledge_details_by_id(knowledge_id=knowledge_id)
    
    product_json = json.dumps(
        knowledge_details.to_dict(),
        ensure_ascii=False,
        indent=2,
        default=str
    )

    user_prompt = USER_PROMPT_TEMPLATE.format(count=count,product_json=product_json)

    response = (
        ollama_service.chat_llm(
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
    )

    generated_ads = json.loads(response.content.strip())
    ads = generated_ads.get("advertisements",[])
    results = []

    for ad in ads:
        strategy = ad.get("strategy", {})       
        creative =  ad.get("creative", {})
        hook = creative.get("hook",{})
        proof =  creative.get("proof", {})
        cta =  creative.get( "cta",{} )
        target = ad.get( "target_audience",{} )
        score = ad.get( "score",  {} )

        advertisement = (
            advertisements_repository.create(
                Advertisement(
                    knowledge_id=knowledge_id,
                    name=ad.get(  "name", ""),
                    strategy_framework=
                    strategy.get( "framework" ),
                    strategy_angle= strategy.get( "angle"),
                    strategy_psychology_trigger=
                    strategy.get( "psychology_trigger"),
                    strategy_awareness_stage=
                    strategy.get( "awareness_stage" ),
                    strategy_hypothesis=
                    strategy.get( "hypothesis" ),

                    platform= creative.get( "platform"),
                    format= creative.get( "format" ),
                    duration_seconds=creative.get( "duration_seconds" ),
                    aspect_ratio= creative.get( "aspect_ratio" ),

                    hook_text=  hook.get( "text" ),
                    hook_type=hook.get( "type" ),
                    hook_visual=  hook.get("visual" ),
                    hook_duration= hook.get( "duration" ),

                    problem= creative.get("problem"),

                    solution=creative.get("solution"),

                    proof_type= proof.get( "type"),
                    proof_content=
                    proof.get("content" ),

                    voiceover= creative.get("voiceover"),

                    audience_description=target.get("name"),

                    cta_text=cta.get("text" ),

                    cta_type=cta.get("type"),

                    cta_urgency=cta.get("urgency"),

                    visual_direction= creative.get( "visual_direction", [] ),

                    text_overlays= creative.get( "text_overlays", [] ),

                    score_hook= score.get( "hook"),
                    score_emotion= score.get( "emotion" ),
                    score_clarity= score.get( "clarity" ),
                    score_purchase_intent= score.get( "purchase_intent"),
                    score_overall= score.get( "overall" )
                )

            )
        )



        #
        # SCENES
        #
        scenes = []
        for scene in creative.get( "scenes",  [] ):
            scenes.append(
                Scene(
                    type=scene.get("type", ""),
                    description= scene.get( "description", "" ),
                    duration_seconds=scene.get( "duration_seconds" )
                )
            )

        saved_scenes = []
        if scenes:
            saved_scenes = scenes_repository.create_many( scenes  )
            
            advertisement_scenes_repository.create_many(
                [
                    AdvertisementScene(
                        advertisement_id=advertisement.id,
                        scene_id=scene.id,
                        order_number= index + 1
                    )

                    for index, scene in enumerate( saved_scenes )
                ]
            )


        #
        # OBJECTIONS
        #
        objections = []
        for objection in ad.get( "objections_handled", [] ):
            objections.append(
                AdvertisementObjection(
                    advertisement_id=advertisement.id,
                    objection= objection.get( "objection", "" ),
                    answer=objection.get( "answer" )
                )
            )

        if objections:
            advertisement_objections_repository.create_many( objections )

        results.append(
            advertisement_service .get_advertisement_details_by_id( id=advertisement.id )
        )

    return results