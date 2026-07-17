import json

from di.container import Container
from domain.models.ollama.llm_ollama_message import LlmOllamaMessage
from domain.enums.ollama_message_role import OllamaMessageRole


# =====================================================
# SALES ASSET SYSTEM PROMPT
# =====================================================

SALES_ASSET_SYSTEM_PROMPT = """
You are a senior direct-response copywriter and conversion strategist.

Your task is to design a complete sales asset (e.g. landing page, advertorial,
VSL script, or email) built from sections.

Each section must include:
- type
- position
- name
- goal
- headline
- subheadline
- content
- an optional visualization describing an image/video that supports the section

Return ONLY valid JSON, no markdown, using this structure:

{
    "name": "",
    "main_angle": "",
    "sections": [
        {
            "type": "",
            "position": 1,
            "name": "",
            "goal": "",
            "headline": "",
            "subheadline": "",
            "content": "",
            "visualization": {
                "format": "",
                "name": "",
                "description": ""
            }
        }
    ]
}
"""


def get_sales_asset_prompt(product_json: str, type: str) -> str:
    return f"""
PRODUCT DATA:

{product_json}

TASK:

Create a complete "{type}" sales asset for this product, following the system instructions.
"""


# =====================================================
# MAIN HANDLER
# =====================================================

def generate_sales_asset_handler(knowledge_id: int, type: str = "landing_page"):

    container = Container()

    logger = container.logger()
    knowledge_service = container.knowledge_service()
    ollama_service = container.ollama_service()

    # ----------------------------
    # LOAD PRODUCT CONTEXT
    # ----------------------------
    assembled_knowledge_dto = knowledge_service.get_knowledge_details_by_id(
        knowledge_id=knowledge_id
    )

    product_json = json.dumps(
        assembled_knowledge_dto.to_dict(),
        ensure_ascii=False,
        indent=2,
    )

    logger.info("Generating sales asset")

    # ----------------------------
    # GENERATE SALES ASSET
    # ----------------------------
    response = ollama_service.chat_llm(
        messages=[
            LlmOllamaMessage(
                role=OllamaMessageRole.SYSTEM,
                content=SALES_ASSET_SYSTEM_PROMPT,
            ),
            LlmOllamaMessage(
                role=OllamaMessageRole.USER,
                content=get_sales_asset_prompt(product_json, type),
            ),
        ]
    )

    try:
        data = json.loads(response.content)
    except Exception:
        data = {"raw_response": response.content}

    logger.info("Sales asset generated")

    return data
