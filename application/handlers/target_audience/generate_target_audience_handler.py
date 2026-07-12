import json
import re
from typing import Dict, Any

from di.container import Container
from application.mappers.offer_knowledge_mapper import OfferKnowledgeMapper

from domain.models.ollama.llm_ollama_message import LlmOllamaMessage
from domain.enums.ollama_message_role import OllamaMessageRole

from domain.enums.audience_gender import AudienceGender
from domain.enums.decision_time import DecisionTime
from domain.enums.awareness_level import AwarenessLevel
from domain.enums.intensity_level import IntensityLevel
from domain.enums.purchasing_power import PurchasingPower

BASE_SYSTEM_PROMPT = """
You are a senior AI product strategy specialist specializing in:

- customer segmentation,
- buying psychology,
- market research,
- ICP (Ideal Customer Profile) definition,
- marketing strategy,
- conversion optimization.

You analyze products and offers and transform product information
into practical customer insights.

Your goal is to determine:

1. Who is most likely to buy the product.
2. Why they will buy it.
3. How to effectively reach them.

Rules:

- Analyze the specific product.
- Do not create generic customer groups.
- Separate facts from assumptions.
- If data is missing, make realistic assumptions.
- Label assumptions.
- Results must be useful for advertising and marketing.

Return ONLY valid JSON.
No markdown.
No comments.
No text outside JSON.
"""


def enum_values(enum):
    return [
        item.value
        for item in enum
    ]


ENUM_PROMPT = f"""
Allowed enum values:

gender:
AudienceGenderEnum:
{enum_values(AudienceGender)}

purchasing_power:
PurchasingPowerEnum:
{enum_values(PurchasingPower)}

awareness_level:
AwarenessLevelEnum:
{enum_values(AwarenessLevel)}

price_sensitivity:
IntensityLevelEnum:
{enum_values(IntensityLevel)}

research_level:
IntensityLevelEnum:
{enum_values(IntensityLevel)}

decision_time:
DecisionTimeEnum:
{enum_values(DecisionTime)}


Enum rules:

- Enum fields must contain a single string value.
- Do not return arrays.
- Do not create new values.
- Use only values available in the corresponding enum.

Correct example:

"gender": "all"

Incorrect example:

"gender": ["male", "female"]
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

            "gender": "",
            "location": "",
            "purchasing_power": "",

            "lifestyles": [""],
            "values": [""],

            "awareness_level": "",
            "price_sensitivity": "",
            "research_level": "",
            "decision_time": "",

            "pain_points": [""],
            "motivations": [""],
            "buying_triggers": [""],
            "objections": [""],

            "message_angles": [""],
            "marketing_channels": [""]
        }
    ]
}



def generate_target_audience_handler(
    offer_id: int,
    knowledge_id: int
) -> Dict[str, Any]:
    container = Container()

    knowledge_repo = container.offer_knowledge_repository()
    knowledge_assembler = container.offer_knowledge_assembler()
    ollama_service = container.ollama_service()

    knowledge_db =  knowledge_repo.get_by_id( id=knowledge_id )

    if not knowledge_db:
        return {
            "status": False,
            "error": "Knowledge not found"
        }


    knowledge_dto = OfferKnowledgeMapper.to_dto( item=knowledge_db )
    assembled_dto =  knowledge_assembler.assemble_dto( item=knowledge_dto )
    knowledge_json = assembled_dto.to_dict()

    schema_json = json.dumps( TARGET_AUDIENCE_SCHEMA, ensure_ascii=False, indent=2)

    user_prompt = f"""
Analyze the product information.

PRODUCT DATA:

{knowledge_json}


Generate target audience segments.


Response format:

{schema_json}


ENUM RULES:

{ENUM_PROMPT}


Requirements:

- Do not invent random customers.
- Provide realistic segments.
- Include assumptions.
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


    response_json = json.loads(response.content )
    audiences_dict = response_json["audiences"]

    return audiences_dict