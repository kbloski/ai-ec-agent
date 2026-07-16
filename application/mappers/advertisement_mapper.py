from domain.models.advertisement.advertisement import Advertisement
from application.dtos.advertisement.advertisement_dto import AdvertisementDto


class AdvertisementMapper:

    @staticmethod
    def to_dto(item: Advertisement) -> AdvertisementDto:
        return AdvertisementDto(
            id=item.id,
            knowledge_id=item.knowledge_id,
            name=item.name,
            strategy_framework=item.strategy_framework,
            strategy_angle=item.strategy_angle,
            strategy_psychology_trigger=item.strategy_psychology_trigger,
            strategy_awareness_stage=item.strategy_awareness_stage,
            strategy_hypothesis=item.strategy_hypothesis,
            platform=item.platform,
            format=item.format,
            duration_seconds=item.duration_seconds,
            aspect_ratio=item.aspect_ratio,
            hook_text=item.hook_text,
            hook_type=item.hook_type,
            hook_visual=item.hook_visual,
            hook_duration=item.hook_duration,
            problem=item.problem,
            solution=item.solution,
            proof_type=item.proof_type,
            proof_content=item.proof_content,
            voiceover=item.voiceover,
            audience_description=item.audience_description,
            cta_text=item.cta_text,
            cta_type=item.cta_type,
            cta_urgency=item.cta_urgency,
            visual_direction=item.visual_direction,
            text_overlays=item.text_overlays,
            score_hook=item.score_hook,
            score_emotion=item.score_emotion,
            score_clarity=item.score_clarity,
            score_purchase_intent=item.score_purchase_intent,
            score_overall=item.score_overall,
        )
