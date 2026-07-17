from typing import Optional, List

from common.mixins.json_serializable import JSONSerializable


class CreativeStrategyDto(JSONSerializable):

    def __init__(
        self,
        id: int,
        knowledge_id: int,
        brand_marketing_id: int,
        marketing_strategy_id: int,
        offer_strategy_id: int,
        message_strategy_id: int,
        ad_strategy_id: int,
        name: Optional[str],
        based_on_ad_concept: Optional[str],
        objective: Optional[str],
        creative_type: Optional[str],
        recommended_format: Optional[str],
        platform: Optional[str],
        duration: Optional[str],
        aspect_ratio: Optional[str],
        target: Optional[dict],
        hook_strategy: Optional[dict],
        story_framework: Optional[List[str]],
        creative_direction: Optional[dict],
        speaker: Optional[dict],
        emotion_flow: Optional[List[str]],
        visual_direction: Optional[List[str]],
        proof_strategy: Optional[List[str]],
        cta_strategy: Optional[dict],
        production_notes: Optional[dict],
    ):
        self.id = id
        self.knowledge_id = knowledge_id
        self.brand_marketing_id = brand_marketing_id
        self.marketing_strategy_id = marketing_strategy_id
        self.offer_strategy_id = offer_strategy_id
        self.message_strategy_id = message_strategy_id
        self.ad_strategy_id = ad_strategy_id
        self.name = name
        self.based_on_ad_concept = based_on_ad_concept
        self.objective = objective
        self.creative_type = creative_type
        self.recommended_format = recommended_format
        self.platform = platform
        self.duration = duration
        self.aspect_ratio = aspect_ratio
        self.target = target
        self.hook_strategy = hook_strategy
        self.story_framework = story_framework
        self.creative_direction = creative_direction
        self.speaker = speaker
        self.emotion_flow = emotion_flow
        self.visual_direction = visual_direction
        self.proof_strategy = proof_strategy
        self.cta_strategy = cta_strategy
        self.production_notes = production_notes

    def to_dict(self, exclude=None):
        exclude = set(exclude or [])

        data = {
            "id": self.id,
            "knowledge_id": self.knowledge_id,
            "brand_marketing_id": self.brand_marketing_id,
            "marketing_strategy_id": self.marketing_strategy_id,
            "offer_strategy_id": self.offer_strategy_id,
            "message_strategy_id": self.message_strategy_id,
            "ad_strategy_id": self.ad_strategy_id,
            "name": self.name,
            "based_on_ad_concept": self.based_on_ad_concept,
            "objective": self.objective,
            "creative_type": self.creative_type,
            "recommended_format": self.recommended_format,
            "platform": self.platform,
            "duration": self.duration,
            "aspect_ratio": self.aspect_ratio,
            "target": self.target,
            "hook_strategy": self.hook_strategy,
            "story_framework": self.story_framework,
            "creative_direction": self.creative_direction,
            "speaker": self.speaker,
            "emotion_flow": self.emotion_flow,
            "visual_direction": self.visual_direction,
            "proof_strategy": self.proof_strategy,
            "cta_strategy": self.cta_strategy,
            "production_notes": self.production_notes,
        }

        return {k: v for k, v in data.items() if k not in exclude}
