import json

from di.container import Container
from domain.models.ollama.llm_ollama_message import LlmOllamaMessage
from domain.enums.ollama_message_role import OllamaMessageRole


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
            "duration_seconds": "",
            "aspect_ratio": "",


            "hook": {{

                "text": "",
                "type": "",
                "visual": "",
                "duration": "0-3s"

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

    return generated_ads.get("advertisements", [])