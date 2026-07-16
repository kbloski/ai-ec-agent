import json

from di.container import Container
from domain.models.ollama.llm_ollama_message import LlmOllamaMessage
from domain.enums.ollama_message_role import OllamaMessageRole
from domain.models.advertisement.advertisement import Advertisement
from domain.models.advertisement.scene import Scene
from domain.models.advertisement.advertisement_scene import AdvertisementScene
from domain.models.advertisement.advertisement_objection import AdvertisementObjection


SYSTEM_PROMPT = """
Jesteś ekspertem od performance marketingu, direct response copywritingu
oraz tworzenia reklam sprzedażowych.

Twoim zadaniem jest generowanie skutecznych kreacji reklamowych na podstawie
danych produktu.

Twoja praca:

1. Przeanalizuj produkt.
2. Znajdź najważniejszy problem klienta.
3. Znajdź emocjonalny trigger zakupu.
4. Wybierz najlepszy format reklamy.
5. Wygeneruj gotową kreację reklamową.

Zasady:

- Klient nie kupuje produktu. Kupuje efekt jaki produkt daje.
- Skupiaj się na problemie, transformacji i korzyściach.
- Hook musi zatrzymać uwagę w pierwszych sekundach.
- Każda reklama musi posiadać:
    - Hook
    - Problem
    - Solution
    - Social Proof
    - CTA

Wykorzystuj formaty:

- Before / After
- Problem Solution
- Product Demo
- Testimonial
- Feature Benefit
- US vs THEM
- Bold Claim
- Offer Sale
- Native

Nie wymyślaj fałszywych danych.
Nie twórz ogólnych reklam.

Każda reklama musi testować inny kąt psychologiczny.

Zwróć odpowiedź wyłącznie jako poprawny JSON.
"""


USER_PROMPT_TEMPLATE = """
Na podstawie poniższych danych produktu wygeneruj {count} różnych kreacji reklamowych.

DANE PRODUKTU:

{product_json}


Zwróć odpowiedź wyłącznie jako poprawny JSON w poniższej strukturze:


[

    {{

        "name": "",
        "strategy": {{
            "framework": "",
            "angle": "",
            "psychology_trigger": "",
            "awareness_stage": "",
            "hypothesis": ""

        }},


        "creative": {{
            "platform": "",
            "format": "",
            "duration_seconds": 15,
            "aspect_ratio": "",


            "hook": {{

                "text": "",
                "type": "",
                "visual": "",
                "duration": 3

            }},


            "problem": "",


            "solution": "",


            "proof": {{

                "type": "",
                "content": ""

            }},


            "script": {{

                "scene_1": "",
                "scene_2": "",
                "scene_3": "",
                "scene_4": "",
                "scene_5": ""

            }},


            "voiceover": "",


            "visual_direction": [

                ""

            ],


            "text_overlays": [

                ""

            ],


            "cta": {{

                "text": "",
                "type": "",
                "urgency": ""

            }}

        }},


        "target_audience": {{

            "name": "",
            "pain_points": [],
            "motivations": [],
            "buying_triggers": []

        }},


        "objections_handled": [

            {{

                "objection": "",
                "answer": ""

            }}

        ],


        "testing": {{

            "variant": "",
            "what_is_tested": "",
            "expected_result": ""

        }},


        "score": {{

            "hook": 0,
            "emotion": 0,
            "clarity": 0,
            "purchase_intent": 0,
            "overall": 0

        }}

    }}

]




ZASADY GENEROWANIA:


1. Wygeneruj dokładnie {count} elementów w tablicy advertisements.


2. Każda reklama musi mieć:
- inny framework reklamowy,
- inny kąt psychologiczny,
- inny hook,
- inną hipotezę marketingową.


3. Wykorzystuj różne strategie:

- Before / After
- Problem → Solution
- Product Demo
- Testimonial
- Feature → Benefit
- US vs THEM
- Bold Claim
- Offer / Sale
- Native
- Statistics
- News Article
- Negative Hook
- What's Inside
- Google Search
- Airdrop


4. Każda reklama musi odpowiadać na:

- Jaki problem klient ma?
- Dlaczego chce go rozwiązać?
- Dlaczego ten produkt jest rozwiązaniem?
- Dlaczego powinien kupić teraz?


5. Hook:

Pierwsze 3 sekundy są najważniejsze.

Hook musi:
- zatrzymać scrollowanie,
- dotyczyć klienta,
- wywoływać emocję,
- być prosty i zrozumiały.


5a. Wartości liczbowe:

Pola "duration_seconds", "hook.duration" oraz wszystkie pola w "score"
(hook, emotion, clarity, purchase_intent, overall) muszą być zwracane
jako liczby całkowite (int), nigdy jako tekst ani zakres czasu.

Poprawnie: "duration_seconds": 15, "duration": 3, "hook": 8
Niepoprawnie: "duration_seconds": "15s", "duration": "0-3s", "hook": "8/10"


6. Copywriting:

Używaj:
- prostego języka,
- krótkich zdań,
- konkretnych korzyści,
- języka klienta.


Nie używaj:
- technicznego żargonu,
- pustych obietnic,
- ogólnych sloganów.


7. Proof:

Jeżeli produkt posiada dane, opinie lub liczby wykorzystaj je.

Nie wymyślaj fałszywych statystyk.


8. CTA:

CTA musi jasno mówić klientowi co zrobić dalej.

Przykłady:
- Sprawdź ofertę
- Zamów teraz
- Zobacz jak działa
- Poznaj szczegóły


9. Oceniaj każdą reklamę:

Skala 1-10.

Oceń:
- siłę hooka,
- emocje,
- prostotę przekazu,
- prawdopodobieństwo zakupu.


10. Nie generuj podobnych reklam.

Każda reklama ma być osobnym eksperymentem marketingowym.
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


    knowledge_details = (
        knowledge_service
        .get_knowledge_details_by_id(
            knowledge_id=knowledge_id
        )
    )


    product_json = json.dumps(
        knowledge_details.to_dict(),
        ensure_ascii=False,
        indent=2
    )


    user_prompt = USER_PROMPT_TEMPLATE.format(
        count=count,
        product_json=product_json
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
        generated_ads = json.loads(
            response.content
        )

    except json.JSONDecodeError:

        return {
            "error": "Invalid JSON from LLM",
            "raw_response": response.content
        }


    if isinstance(generated_ads, list):
        ads = generated_ads
    else:
        ads = generated_ads.get("advertisements", [])

    results = []

    for ad in ads:
        strategy = ad.get("strategy", {}) or {}
        creative = ad.get("creative", {}) or {}
        hook = creative.get("hook", {}) or {}
        proof = creative.get("proof", {}) or {}
        script = creative.get("script", {}) or {}
        cta = creative.get("cta", {}) or {}
        target_audience = ad.get("target_audience", {}) or {}
        score = ad.get("score", {}) or {}

        advertisement = advertisements_repository.create(
            Advertisement(
                knowledge_id=knowledge_id,
                name=ad.get("name", ""),
                strategy_framework=strategy.get("framework"),
                strategy_angle=strategy.get("angle"),
                strategy_psychology_trigger=strategy.get("psychology_trigger"),
                strategy_awareness_stage=strategy.get("awareness_stage"),
                strategy_hypothesis=strategy.get("hypothesis"),
                platform=creative.get("platform"),
                format=creative.get("format"),
                duration_seconds=creative.get("duration_seconds") or None,
                aspect_ratio=creative.get("aspect_ratio"),
                hook_text=hook.get("text"),
                hook_type=hook.get("type"),
                hook_visual=hook.get("visual"),
                hook_duration=hook.get("duration") or None,
                problem=creative.get("problem"),
                solution=creative.get("solution"),
                proof_type=proof.get("type"),
                proof_content=proof.get("content"),
                voiceover=creative.get("voiceover"),
                audience_description=target_audience.get("name"),
                cta_text=cta.get("text"),
                cta_type=cta.get("type"),
                cta_urgency=cta.get("urgency"),
                visual_direction=creative.get("visual_direction"),
                text_overlays=creative.get("text_overlays"),
                score_hook=score.get("hook"),
                score_emotion=score.get("emotion"),
                score_clarity=score.get("clarity"),
                score_purchase_intent=score.get("purchase_intent"),
                score_overall=score.get("overall"),
            )
        )

        scene_models = [
            Scene(type="scene", description=script[key], duration_seconds=None)
            for key in sorted(script.keys())
            if script.get(key)
        ]
        saved_scenes = scenes_repository.create_many(scene_models)

        advertisement_scenes_repository.create_many(
            [
                AdvertisementScene(
                    advertisement_id=advertisement.id,
                    scene_id=scene.id,
                    order_number=index + 1,
                )
                for index, scene in enumerate(saved_scenes)
            ]
        )

        advertisement_objections_repository.create_many(
            [
                AdvertisementObjection(
                    advertisement_id=advertisement.id,
                    objection=objection.get("objection", ""),
                    answer=objection.get("answer"),
                )
                for objection in ad.get("objections_handled", [])
            ]
        )

        results.append(
            advertisement_service.get_advertisement_details_by_id(id=advertisement.id)
        )

    return results