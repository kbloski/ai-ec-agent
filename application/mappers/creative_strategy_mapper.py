from domain.models.creative_strategy.creative_strategy import CreativeStrategy
from application.dtos.creative_strategy.creative_strategy_response_dto import CreativeStrategyDto


class CreativeStrategyMapper:

    @staticmethod
    def to_dto(item: CreativeStrategy) -> CreativeStrategyDto:
        return CreativeStrategyDto(
            id=item.id,
            knowledge_id=item.knowledge_id,
            brand_marketing_id=item.brand_marketing_id,
            marketing_strategy_id=item.marketing_strategy_id,
            offer_strategy_id=item.offer_strategy_id,
            message_strategy_id=item.message_strategy_id,
            ad_strategy_id=item.ad_strategy_id,
            name=item.name,
            execution=item.execution,
            script=item.script,
            asset_requirements=item.asset_requirements,
            production_notes=item.production_notes,
            cta=item.cta,
        )
