from domain.models.ad_strategy.ad_strategy import AdStrategy
from application.dtos.ad_strategy.ad_strategy_response_dto import AdStrategyDto


class AdStrategyMapper:

    @staticmethod
    def to_dto(item: AdStrategy) -> AdStrategyDto:
        return AdStrategyDto(
            id=item.id,
            knowledge_id=item.knowledge_id,
            brand_marketing_id=item.brand_marketing_id,
            marketing_strategy_id=item.marketing_strategy_id,
            offer_strategy_id=item.offer_strategy_id,
            message_strategy_id=item.message_strategy_id,
            objective=item.objective,
            customer_stage=item.customer_stage,
            priority_audiences=item.priority_audiences,
            audience_angles=item.audience_angles,
            message_angles=item.message_angles,
            offer_angles=item.offer_angles,
            creative_concepts=item.creative_concepts,
            recommended_formats=item.recommended_formats,
            testing_hypotheses=item.testing_hypotheses,
        )
