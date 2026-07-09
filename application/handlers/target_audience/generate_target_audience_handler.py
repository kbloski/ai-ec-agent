import json
import re
from typing import Dict, Any

from di.container import Container
from application.mappers.offer_knowledge_mapper import OfferKnowledgeMapper

from domain.models.ollama.llm_ollama_message import LlmOllamaMessage
from domain.enums.ollama.ollama_message_role import OllamaMessageRole
from domain.enums.gender import Gender


BASE_SYSTEM_PROMPT = """
Jesteś seniorem strategii produktowej AI specjalizującym się w:

- segmentacji klientów,
- psychologii zakupowej,
- badaniu rynku,
- definiowaniu ICP,
- strategii marketingowej,
- optymalizacji konwersji.

Analizujesz produkty i oferty oraz zamieniasz informacje o produkcie
w praktyczne dane o klientach.

Twoim celem jest określenie:

1. Kto najprawdopodobniej kupi produkt.
2. Dlaczego go kupi.
3. Jak skutecznie do niego dotrzeć.

Zasady:

- Analizuj konkretny produkt.
- Nie twórz generycznych grup klientów.
- Oddziel fakty od założeń.
- Jeśli brakuje danych, wykonaj realistyczne założenia.
- Oznacz założenia.
- Wyniki muszą być użyteczne reklamowo.

Zwróć WYŁĄCZNIE poprawny JSON.
Bez markdown.
Bez komentarzy.
Bez tekstu poza JSON.
"""

TARGET_AUDIENCE_SCHEMA = {
    "audiences": [
        {
            "name": "",
            "score": 0,
            "confidence": 0,
            "reason": "",

            "age_min": 0,
            "age_max": 0,
            "gender": "all",

            "location": "",
            "purchasing_power": "",

            "lifestyles": ["string"],
            "values": ["string"],

            "awareness_level": "",
            "price_sensitivity": "",
            "research_level": "",
            "decision_time": "",

            "pain_points": ["string"],
            "motivations": ["string"],
            "buying_triggers": ["string"],
            "objections": ["string"],

            "message_angles": ["string"],
            "marketing_channels": ["string"]
        }
    ]
}


def serialize_object(obj):

    if isinstance(obj, list):
        return [
            serialize_object(x)
            for x in obj
        ]

    if isinstance(obj, dict):
        return {
            k: serialize_object(v)
            for k, v in obj.items()
        }

    if hasattr(obj, "__dict__"):
        return {
            key: serialize_object(value)
            for key, value in obj.__dict__.items()
            if not key.startswith("_")
        }

    return obj


def extract_json(text: str):

    """
    Wyciąga JSON jeśli model dodał tekst przed/po JSON.
    """

    match = re.search(
        r"\{.*\}",
        text,
        re.DOTALL
    )

    if not match:
        raise ValueError(
            "LLM response does not contain JSON"
        )

    return match.group(0)



def generate_target_audience_handler(
    offer_id: int,
    knowledge_id: int
) -> Dict[str, Any]:


    container = Container()


    knowledge_repo = (
        container.offer_knowledge_repository()
    )

    knowledge_assembler = (
        container.offer_knowledge_assembler()
    )

    ollama_service = (
        container.ollama_service()
    )


    knowledge_db = (
        knowledge_repo.get_by_id(
            id=knowledge_id
        )
    )


    if not knowledge_db:
        return {
            "status": False,
            "error": "Knowledge not found"
        }


    knowledge_dto = (
        OfferKnowledgeMapper.to_dto(
            item=knowledge_db
        )
    )


    assembled_dto = (
        knowledge_assembler.assemble_dto(
            item=knowledge_dto
        )
    )


    knowledge_json = json.dumps(
        serialize_object(
            assembled_dto
        ),
        ensure_ascii=False,
        indent=2
    )


    schema_json = json.dumps(
        TARGET_AUDIENCE_SCHEMA,
        ensure_ascii=False,
        indent=2
    )


    user_prompt = f"""
Przeanalizuj informacje o produkcie.

DANE PRODUKTU:

{knowledge_json}


Wygeneruj grupy docelowe.

Odpowiedź musi dokładnie pasować do tego JSON:

{schema_json}


Wymagania:

- Odpowiedź po polsku.
- Nie wymyślaj przypadkowych klientów.
- Podawaj realistyczne segmenty.
- Uwzględnij założenia.
- JSON ONLY.
"""


    response = ollama_service.chat_llm(
        messages=[

            LlmOllamaMessage(
                role=OllamaMessageRole.SYSTEM,
                content=BASE_SYSTEM_PROMPT
            ),

            LlmOllamaMessage(
                role=OllamaMessageRole.USER,
                content=user_prompt
            )
        ]
    )


    try:

        clean_json = extract_json(
            response.content
        )

        response_json = json.loads(
            clean_json
        )

    except Exception as e:

        return {
            "status": False,
            "error": "Invalid LLM JSON",
            "raw_response": response.content,
            "details": str(e)
        }


    return {
        "status": True,
        "data": response_json
    }