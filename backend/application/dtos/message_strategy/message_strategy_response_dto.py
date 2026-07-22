from typing import Optional, List

from common.mixins.json_serializable import JSONSerializable


class MessageStrategyDto(JSONSerializable):

    def __init__(
        self,
        id: int,
        offer_strategy_id: int,
        core_message: Optional[str],
        brand_message: Optional[str],
        primary_message_angle: Optional[str],
        secondary_message_angles: Optional[List[str]],
        audience_messages: Optional[List[str]],
        customer_pain_points: Optional[List[str]],
        customer_desires: Optional[List[str]],
        benefit_messages: Optional[List[str]],
        feature_to_benefit_mapping: Optional[List[str]],
        objection_handling_messages: Optional[List[str]],
        trust_messages: Optional[List[str]],
        proof_points: Optional[List[str]],
        emotional_triggers: Optional[List[str]],
        rational_arguments: Optional[List[str]],
        advertising_angles: Optional[List[str]],
        content_angles: Optional[List[str]],
        ugc_angles: Optional[List[str]],
    ):
        self.id = id
        self.offer_strategy_id = offer_strategy_id
        self.core_message = core_message
        self.brand_message = brand_message
        self.primary_message_angle = primary_message_angle
        self.secondary_message_angles = secondary_message_angles
        self.audience_messages = audience_messages
        self.customer_pain_points = customer_pain_points
        self.customer_desires = customer_desires
        self.benefit_messages = benefit_messages
        self.feature_to_benefit_mapping = feature_to_benefit_mapping
        self.objection_handling_messages = objection_handling_messages
        self.trust_messages = trust_messages
        self.proof_points = proof_points
        self.emotional_triggers = emotional_triggers
        self.rational_arguments = rational_arguments
        self.advertising_angles = advertising_angles
        self.content_angles = content_angles
        self.ugc_angles = ugc_angles

    def to_dict(self, exclude=None):
        exclude = set(exclude or [])

        data = {
            "id": self.id,
            "offer_strategy_id": self.offer_strategy_id,
            "core_message": self.core_message,
            "brand_message": self.brand_message,
            "primary_message_angle": self.primary_message_angle,
            "secondary_message_angles": self.secondary_message_angles,
            "audience_messages": self.audience_messages,
            "customer_pain_points": self.customer_pain_points,
            "customer_desires": self.customer_desires,
            "benefit_messages": self.benefit_messages,
            "feature_to_benefit_mapping": self.feature_to_benefit_mapping,
            "objection_handling_messages": self.objection_handling_messages,
            "trust_messages": self.trust_messages,
            "proof_points": self.proof_points,
            "emotional_triggers": self.emotional_triggers,
            "rational_arguments": self.rational_arguments,
            "advertising_angles": self.advertising_angles,
            "content_angles": self.content_angles,
            "ugc_angles": self.ugc_angles,
        }

        return {k: v for k, v in data.items() if k not in exclude}
