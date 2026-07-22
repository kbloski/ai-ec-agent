from domain.models.message_strategy.message_strategy import MessageStrategy
from application.dtos.message_strategy.message_strategy_response_dto import MessageStrategyDto


class MessageStrategyMapper:

    @staticmethod
    def to_dto(item: MessageStrategy) -> MessageStrategyDto:
        return MessageStrategyDto(
            id=item.id,
            offer_strategy_id=item.offer_strategy_id,
            core_message=item.core_message,
            brand_message=item.brand_message,
            primary_message_angle=item.primary_message_angle,
            secondary_message_angles=item.secondary_message_angles,
            audience_messages=item.audience_messages,
            customer_pain_points=item.customer_pain_points,
            customer_desires=item.customer_desires,
            benefit_messages=item.benefit_messages,
            feature_to_benefit_mapping=item.feature_to_benefit_mapping,
            objection_handling_messages=item.objection_handling_messages,
            trust_messages=item.trust_messages,
            proof_points=item.proof_points,
            emotional_triggers=item.emotional_triggers,
            rational_arguments=item.rational_arguments,
            advertising_angles=item.advertising_angles,
            content_angles=item.content_angles,
            ugc_angles=item.ugc_angles,
        )
