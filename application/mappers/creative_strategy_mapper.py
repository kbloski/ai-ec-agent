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
            based_on_ad_concept=item.based_on_ad_concept,
            objective=item.objective,
            creative_type=item.creative_type,
            recommended_format=item.recommended_format,
            platform=item.platform,
            duration=item.duration,
            aspect_ratio=item.aspect_ratio,
            target=item.target,
            hook_strategy=item.hook_strategy,
            story_framework=item.story_framework,
            creative_direction=item.creative_direction,
            speaker=item.speaker,
            emotion_flow=item.emotion_flow,
            visual_direction=item.visual_direction,
            proof_strategy=item.proof_strategy,
            cta_strategy=item.cta_strategy,
            production_notes=item.production_notes,
        )
