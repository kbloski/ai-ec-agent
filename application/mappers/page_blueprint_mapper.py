from domain.models.page_blueprint.page_blueprint import PageBlueprint
from application.dtos.page_blueprint.page_blueprint_response_dto import PageBlueprintDto


class PageBlueprintMapper:

    @staticmethod
    def to_dto(item: PageBlueprint) -> PageBlueprintDto:
        return PageBlueprintDto(
            id=item.id,
            knowledge_id=item.knowledge_id,
            brand_marketing_id=item.brand_marketing_id,
            marketing_strategy_id=item.marketing_strategy_id,
            offer_strategy_id=item.offer_strategy_id,
            message_strategy_id=item.message_strategy_id,
            page_strategy_id=item.page_strategy_id,
            page_type=item.page_type,
            primary_conversion_goal=item.primary_conversion_goal,
            sections=item.sections,
        )
