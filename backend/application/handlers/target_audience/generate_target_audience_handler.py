import json
import re
from typing import Dict, Any

from di.container import Container
from application.mappers.offer_knowledge_mapper import OfferKnowledgeMapper
from application.mappers.target_audience_mapper import TargetAudienceMapper

from domain.models.ollama.llm_ollama_message import LlmOllamaMessage
from domain.models.audience.target_audience import TargetAudience

from domain.enums.ollama_message_role import OllamaMessageRole
from domain.enums.audience_gender import AudienceGender
from domain.enums.decision_time import DecisionTime
from domain.enums.awareness_level import AwarenessLevel
from domain.enums.intensity_level import IntensityLevel
from domain.enums.purchasing_power import PurchasingPower
from domain.enums.content_status import ContentStatus

from infrastructure.ai.prompts.constraints.uniqueness_prompt import build_uniqueness_constraint_prompt

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

Requirements:
- confidence MUST be a float between 0 and 1.
- score MUST be an integer between 0 and 1.

Return ONLY valid JSON.
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
    knowledge_id: int
) -> Dict[str, Any]:
    container = Container()

    target_audience_repo = container.target_audiences_repository()
    ollama_service = container.ollama_service()
    knowledge_service = container.knowledge_service()

    target_audiences_db = target_audience_repo.find_for_knowledge(knowledge_id=knowledge_id)
    target_audiences_db_dtos = [TargetAudienceMapper.to_dto(item=t) for t in target_audiences_db]
    knowledge_json = knowledge_service.get_knowledge_details_by_id(knowledge_id=knowledge_id).to_dict()

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
- Return a minimum of 3 target audience segments.
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
                content=build_uniqueness_constraint_prompt(
                    existing_data= json.dumps( [t.to_dict() for t in target_audiences_db_dtos])
                )
            ),
            LlmOllamaMessage(
                role=OllamaMessageRole.USER,
                content=user_prompt
            )
        ]
    )


    response_json = json.loads(response.content )
    audiences_arr = response_json["audiences"]

    new_target_audiences = []
    for t in audiences_arr:
        new_target_audiences.append(
            TargetAudience(
                knowledge_id=knowledge_id,
                content_status=ContentStatus.SUGGESTED.value,
                name=t["name"],
                reason=t["reason"],
                score=t['score'],
                confidence=t['confidence'],
                age_min=t["age_min"],
                age_max=t["age_max"],
                gender=t["gender"],
                location=t["location"],
                purchasing_power=t["purchasing_power"],
                lifestyles=t["lifestyles"],
                values=t["values"],
                awareness_level=t["awareness_level"],
                price_sensitivity=t["price_sensitivity"],
                research_level=t["research_level"],
                decision_time=t["decision_time"],
                pain_points=t["pain_points"],
                motivations=t["motivations"],
                buying_triggers=t["buying_triggers"],
                objections=t["objections"],
                message_angles=t["message_angles"],
                marketing_channels=t["marketing_channels"]
            )
        )

    target_audience_repo.create_many(items=new_target_audiences)

    return new_target_audiences