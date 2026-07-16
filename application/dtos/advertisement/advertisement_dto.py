from typing import List, Optional

from common.mixins.json_serializable import JSONSerializable
from application.dtos.advertisement.advertisement_scene_dto import AdvertisementSceneDto
from application.dtos.advertisement.advertisement_visualization_dto import (
    AdvertisementVisualizationDto,
)
from application.dtos.advertisement.advertisement_objection_dto import AdvertisementObjectionDto


class AdvertisementDto(JSONSerializable):
    scenes: List[AdvertisementSceneDto] = []
    visualizations: List[AdvertisementVisualizationDto] = []
    objections: List[AdvertisementObjectionDto] = []

    def __init__(
        self,
        id: int,
        knowledge_id: int,
        name: str,
        strategy_framework: Optional[str],
        strategy_angle: Optional[str],
        strategy_psychology_trigger: Optional[str],
        strategy_awareness_stage: Optional[str],
        strategy_hypothesis: Optional[str],
        platform: Optional[str],
        format: Optional[str],
        duration_seconds: Optional[int],
        aspect_ratio: Optional[str],
        hook_text: Optional[str],
        hook_type: Optional[str],
        hook_visual: Optional[str],
        hook_duration: Optional[int],
        problem: Optional[str],
        solution: Optional[str],
        proof_type: Optional[str],
        proof_content: Optional[str],
        voiceover: Optional[str],
        audience_description: Optional[str],
        cta_text: Optional[str],
        cta_type: Optional[str],
        cta_urgency: Optional[str],
        visual_direction: Optional[list],
        text_overlays: Optional[list],
        score_hook: Optional[int],
        score_emotion: Optional[int],
        score_clarity: Optional[int],
        score_purchase_intent: Optional[int],
        score_overall: Optional[int],
    ):
        self.id = id
        self.knowledge_id = knowledge_id
        self.name = name
        self.strategy_framework = strategy_framework
        self.strategy_angle = strategy_angle
        self.strategy_psychology_trigger = strategy_psychology_trigger
        self.strategy_awareness_stage = strategy_awareness_stage
        self.strategy_hypothesis = strategy_hypothesis
        self.platform = platform
        self.format = format
        self.duration_seconds = duration_seconds
        self.aspect_ratio = aspect_ratio
        self.hook_text = hook_text
        self.hook_type = hook_type
        self.hook_visual = hook_visual
        self.hook_duration = hook_duration
        self.problem = problem
        self.solution = solution
        self.proof_type = proof_type
        self.proof_content = proof_content
        self.voiceover = voiceover
        self.audience_description = audience_description
        self.cta_text = cta_text
        self.cta_type = cta_type
        self.cta_urgency = cta_urgency
        self.visual_direction = visual_direction
        self.text_overlays = text_overlays
        self.score_hook = score_hook
        self.score_emotion = score_emotion
        self.score_clarity = score_clarity
        self.score_purchase_intent = score_purchase_intent
        self.score_overall = score_overall

    def to_dict(self, exclude=None):
        exclude = set(exclude or [])

        data = {
            "id": self.id,
            "knowledge_id": self.knowledge_id,
            "name": self.name,
            "strategy_framework": self.strategy_framework,
            "strategy_angle": self.strategy_angle,
            "strategy_psychology_trigger": self.strategy_psychology_trigger,
            "strategy_awareness_stage": self.strategy_awareness_stage,
            "strategy_hypothesis": self.strategy_hypothesis,
            "platform": self.platform,
            "format": self.format,
            "duration_seconds": self.duration_seconds,
            "aspect_ratio": self.aspect_ratio,
            "hook_text": self.hook_text,
            "hook_type": self.hook_type,
            "hook_visual": self.hook_visual,
            "hook_duration": self.hook_duration,
            "problem": self.problem,
            "solution": self.solution,
            "proof_type": self.proof_type,
            "proof_content": self.proof_content,
            "voiceover": self.voiceover,
            "audience_description": self.audience_description,
            "cta_text": self.cta_text,
            "cta_type": self.cta_type,
            "cta_urgency": self.cta_urgency,
            "visual_direction": self.visual_direction,
            "text_overlays": self.text_overlays,
            "score_hook": self.score_hook,
            "score_emotion": self.score_emotion,
            "score_clarity": self.score_clarity,
            "score_purchase_intent": self.score_purchase_intent,
            "score_overall": self.score_overall,
            "scenes": [item.to_dict() for item in self.scenes],
            "visualizations": [item.to_dict() for item in self.visualizations],
            "objections": [item.to_dict() for item in self.objections],
        }

        return {k: v for k, v in data.items() if k not in exclude}
