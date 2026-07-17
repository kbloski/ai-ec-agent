from domain.models.marketing_strategy.marketing_strategy import MarketingStrategy
from application.dtos.marketing_strategy.marketing_strategy_response_dto import MarketingStrategyDto


class MarketingStrategyMapper:

    @staticmethod
    def to_dto(item: MarketingStrategy) -> MarketingStrategyDto:
        return MarketingStrategyDto(
            id=item.id,
            knowledge_id=item.knowledge_id,
            brand_marketing_id=item.brand_marketing_id,
            marketing_objective=item.marketing_objective,
            growth_strategy=item.growth_strategy,
            primary_audience=item.primary_audience,
            secondary_audience=item.secondary_audience,
            audience_prioritization=item.audience_prioritization,
            customer_journey=item.customer_journey,
            marketing_channels=item.marketing_channels,
            acquisition_strategy=item.acquisition_strategy,
            trust_building_strategy=item.trust_building_strategy,
            content_strategy=item.content_strategy,
            community_strategy=item.community_strategy,
            creator_influencer_strategy=item.creator_influencer_strategy,
            campaign_directions=item.campaign_directions,
            conversion_strategy=item.conversion_strategy,
            retention_strategy=item.retention_strategy,
            marketing_experiments=item.marketing_experiments,
            marketing_kpis=item.marketing_kpis,
        )
