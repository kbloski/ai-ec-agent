from domain.models.video_creative_execution.video_creative_execution import VideoCreativeExecution
from application.dtos.video_creative_execution.video_creative_execution_response_dto import VideoCreativeExecutionDto


class VideoCreativeExecutionMapper:

    @staticmethod
    def to_dto(item: VideoCreativeExecution) -> VideoCreativeExecutionDto:
        return VideoCreativeExecutionDto(
            id=item.id,
            ad_execution_id=item.ad_execution_id,
            duration_seconds=item.duration_seconds,
            hook_strategy=item.hook_strategy,
            structure=item.structure,
            scenes=item.scenes,
            asset_requirements=item.asset_requirements,
            production_notes=item.production_notes,
            cta=item.cta,
        )
