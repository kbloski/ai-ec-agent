import json

from di.container import Container
from domain.models.ollama.llm_ollama_message import LlmOllamaMessage
from domain.enums.ollama_message_role import OllamaMessageRole
from domain.models.sales_assets.sales_assets import SalesAsset
from domain.models.sales_assets.sales_asset_sections import SalesAssetSection
from domain.models.sales_assets.sales_asset_section_visualization import (
    SalesAssetSectionVisualization,
)
from domain.models.visualizations.vusualization import Visualization
from application.mappers.sales_asset_mapper import SalesAssetMapper


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

    sales_assets_repository = container.sales_assets_repository()
    sales_asset_sections_repository = container.sales_asset_sections_repository()
    visualizations_repository = container.visualizations_repository()
    sales_asset_section_visualizations_repository = (
        container.sales_asset_section_visualizations_repository()
    )
    sales_asset_assembler = container.sales_asset_assembler()

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

    # ----------------------------
    # SAVE TO DATABASE
    # ----------------------------
    sales_asset = sales_assets_repository.create(
        SalesAsset(
            knowledge_id=knowledge_id,
            type=type,
            name=data.get("name", ""),
            main_angle=data.get("main_angle"),
            content_status="draft",
            version=1,
        )
    )

    raw_sections = data.get("sections", [])

    section_models = [
        SalesAssetSection(
            sales_asset_id=sales_asset.id,
            type=section.get("type", ""),
            position=section.get("position", index + 1),
            name=section.get("name", ""),
            goal=section.get("goal"),
            headline=section.get("headline"),
            subheadline=section.get("subheadline"),
            content=section.get("content"),
        )
        for index, section in enumerate(raw_sections)
    ]

    saved_sections = sales_asset_sections_repository.create_many(section_models)

    for section, saved_section in zip(raw_sections, saved_sections):
        visualization_data = section.get("visualization")

        if not visualization_data:
            continue

        visualization = visualizations_repository.create(
            Visualization(
                format=visualization_data.get("format", ""),
                name=visualization_data.get("name", ""),
                description=visualization_data.get("description", ""),
            )
        )

        sales_asset_section_visualizations_repository.upsert(
            SalesAssetSectionVisualization(
                sales_asset_section_id=saved_section.id,
                visualization_id=visualization.id,
                position=1,
            )
        )

    # ----------------------------
    # PREPARE DTO RESULT
    # ----------------------------
    result_dto = SalesAssetMapper.to_dto(sales_asset)
    result = sales_asset_assembler.assemble_dto(result_dto)

    return result
