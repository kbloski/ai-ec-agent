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
            objective=item.objective,
            creative_type=item.creative_type,
            recommended_format=item.recommended_format,
            target=item.target,
            creative_big_idea=item.creative_big_idea,
            message_angle=item.message_angle,
            hook_strategy=item.hook_strategy,
            story_framework=item.story_framework,
            creative_direction=item.creative_direction,
            speaker_strategy=item.speaker_strategy,
            emotion_flow=item.emotion_flow,
            proof_strategy=item.proof_strategy,
            execution_guidelines=item.execution_guidelines,
        )
