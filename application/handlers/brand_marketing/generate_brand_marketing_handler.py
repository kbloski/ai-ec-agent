import json

from di.container import Container
from domain.models.ollama.llm_ollama_message import LlmOllamaMessage
from domain.enums.ollama_message_role import OllamaMessageRole


SYSTEM_PROMPT = """
Jesteś ekspertem od brand strategy oraz brand marketingu.

Twoim zadaniem jest przeanalizowanie danych knowledge base:
- produktu,
- grup docelowych,
- customer voice,
- problemów klientów,
- obiekcji,
- potrzeb,
- wartości klientów,
- analizy rynku.

Na tej podstawie wygeneruj fundament strategii marki.

Nie tworzysz:
- reklam,
- kampanii sprzedażowych,
- CTA,
- konkretnych kreacji reklamowych.

Tworzysz fundament marki, który będzie później używany przez:
- marketing strategy,
- offer strategy,
- message strategy,
- ads generation,
- landing page generation,
- content generation,
- UGC generation.

Każda decyzja musi wynikać z danych wejściowych.
Nie wymyślaj losowych wartości, które nie wynikają z analizy produktu i klienta.


Twoja odpowiedź musi zawierać:

- nazwę marki,
- pozycjonowanie,
- wyróżnienie konkurencyjne,
- osobowość marki,
- wartości,
- sposób komunikacji,
- emocje,
- percepcję klienta,
- psychologię klienta,
- historię marki,
- kierunki contentu,
- zasady komunikacji.


Zwróć wyłącznie poprawny JSON w dokładnie tej strukturze:

{
    "brand_name": "",

    "brand_positioning": "",
    "brand_category": "",
    "brand_target_customer": "",
    "brand_competitive_difference": "",

    "brand_purpose": "",
    "brand_promise": "",

    "brand_personality": [
        ""
    ],

    "brand_values": [
        ""
    ],

    "brand_voice": "",

    "brand_tone": "",

    "brand_tone_social_media": "",

    "brand_tone_customer_communication": "",

    "tagline": "",

    "unique_selling_proposition": "",

    "key_messages": [
        ""
    ],

    "target_perception": [
        ""
    ],

    "target_emotions": [
        ""
    ],

    "brand_associations": [
        ""
    ],

    "customer_desires": [
        ""
    ],

    "customer_pains": [
        ""
    ],

    "customer_fears": [
        ""
    ],

    "customer_objections": [
        ""
    ],

    "purchase_motivators": [
        ""
    ],

    "brand_story": "",

    "brand_story_angle": "",

    "customer_transformation": "",

    "content_pillars": [
        ""
    ],

    "storytelling_angles": [
        ""
    ],

    "ugc_direction": [
        ""
    ],

    "visual_style": "",

    "visual_direction": "",

    "brand_always_do": [
        ""
    ],

    "brand_never_do": [
        ""
    ]
}


Nie dodawaj:
- markdown,
- ```json,
- komentarzy,
- opisów przed JSON.
"""


USER_PROMPT_TEMPLATE = """
Na podstawie poniższych danych knowledge base wygeneruj strategię marki.

DANE KNOWLEDGE BASE:

{knowledge_json}
"""


def generate_brand_marketing_handler(
    knowledge_id: int
):
    container = Container()

    knowledge_service = container.knowledge_service()
    ollama_service = container.ollama_service()

    knowledge_details = knowledge_service.get_knowledge_details_by_id(
        knowledge_id=knowledge_id
    )

    knowledge_json = json.dumps(
        knowledge_details.to_dict(),
        ensure_ascii=False,
        indent=2,
        default=str
    )

    user_prompt = USER_PROMPT_TEMPLATE.format(
        knowledge_json=knowledge_json
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

    return json.loads(response.content.strip())