from typing import Optional, List

from common.mixins.json_serializable import JSONSerializable


class CreativeStrategyDto(JSONSerializable):

    def __init__(
        self,
        id: int,
        ad_strategy_id: int,
        name: Optional[str],
        objective: Optional[str],
        creative_type: Optional[str],
        recommended_format: Optional[str],
        target: Optional[dict],
        creative_big_idea: Optional[str],
        message_angle: Optional[str],
        hook_strategy: Optional[dict],
        story_framework: Optional[List[str]],
        creative_direction: Optional[dict],
        speaker_strategy: Optional[dict],
        emotion_flow: Optional[List[str]],
        proof_strategy: Optional[List[str]],
        execution_guidelines: Optional[dict],
    ):
        self.id = id
        self.ad_strategy_id = ad_strategy_id
        self.name = name
        self.objective = objective
        self.creative_type = creative_type
        self.recommended_format = recommended_format
        self.target = target
        self.creative_big_idea = creative_big_idea
        self.message_angle = message_angle
        self.hook_strategy = hook_strategy
        self.story_framework = story_framework
        self.creative_direction = creative_direction
        self.speaker_strategy = speaker_strategy
        self.emotion_flow = emotion_flow
        self.proof_strategy = proof_strategy
        self.execution_guidelines = execution_guidelines

    def to_dict(self, exclude=None):
        exclude = set(exclude or [])

        data = {
            "id": self.id,
            "ad_strategy_id": self.ad_strategy_id,
            "name": self.name,
            "objective": self.objective,
            "creative_type": self.creative_type,
            "recommended_format": self.recommended_format,
            "target": self.target,
            "creative_big_idea": self.creative_big_idea,
            "message_angle": self.message_angle,
            "hook_strategy": self.hook_strategy,
            "story_framework": self.story_framework,
            "creative_direction": self.creative_direction,
            "speaker_strategy": self.speaker_strategy,
            "emotion_flow": self.emotion_flow,
            "proof_strategy": self.proof_strategy,
            "execution_guidelines": self.execution_guidelines,
        }

        return {k: v for k, v in data.items() if k not in exclude}
