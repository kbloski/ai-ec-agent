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


Zwróć JSON w strukturze:

{{
    "product_analysis": {{
        "main_problem": "",
        "customer_desire": "",
        "main_emotion": "",
        "main_objection": "",
        "transformation": ""
    }},

    "advertisements": [
        {{
            "name": "",
            "angle": "",
            "format": "",
            "target_audience": "",

            "hook": "",

            "script": {{
                "scene_1": "",
                "scene_2": "",
                "scene_3": "",
                "scene_4": "",
                "scene_5": ""
            }},

            "visual_direction": [
                ""
            ],

            "text_overlays": [
                ""
            ],

            "cta": ""
        }}
    ]
}}


Ważne:
- Tablica advertisements musi zawierać dokładnie {count} elementów.
- Każda reklama musi mieć inny kąt psychologiczny.
- Nie kopiuj tych samych hooków.
- Nie kopiuj tych samych scenariuszy.
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

        generated_ads = {
            "error": "Invalid JSON from LLM",
            "raw_response": response.content
        }


    return {
        "knowledge_id": knowledge_id,
        "count": count,
        "generated": generated_ads
    }