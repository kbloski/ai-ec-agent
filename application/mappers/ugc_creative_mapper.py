from domain.models.ugc_creatives.ugc_creative import UgcCreative
from application.dtos.ugc_creatives.ugc_creative_response_dto import UgcCreativeDto


class UgcCreativeMapper:

    @staticmethod
    def to_dto(item: UgcCreative) -> UgcCreativeDto:
        return UgcCreativeDto(
            id=item.id,
            knowledge_id=item.knowledge_id,
            brand_marketing_id=item.brand_marketing_id,
            marketing_strategy_id=item.marketing_strategy_id,
            offer_strategy_id=item.offer_strategy_id,
            message_strategy_id=item.message_strategy_id,
            name=item.name,
            customer_persona=item.customer_persona,
            content_format=item.content_format,
            angle=item.angle,
            hook_idea=item.hook_idea,
            video_flow=item.video_flow,
            recording_style=item.recording_style,
            platform_fit=item.platform_fit,
            cta=item.cta,
            why_it_should_work=item.why_it_should_work,
        )
