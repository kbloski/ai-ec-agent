from typing import List

from infrastructure.logging.logger import Logger
from domain.models.video_creative_execution.video_creative_execution import VideoCreativeExecution
from application.dtos.video_creative_execution.video_creative_execution_response_dto import VideoCreativeExecutionDto
from infrastructure.repositories.video_creative_execution_repository import VideoCreativeExecutionRepository
from application.mappers.video_creative_execution_mapper import VideoCreativeExecutionMapper
from application.assemblers.video_creative_execution_assembler import VideoCreativeExecutionAssembler


class VideoCreativeExecutionService:

    def __init__(
        self,
        logger: Logger,
        video_creative_execution_repository: VideoCreativeExecutionRepository,
        video_creative_execution_assembler: VideoCreativeExecutionAssembler,
    ):
        self.logger = logger
        self.video_creative_execution_repository = video_creative_execution_repository
        self.video_creative_execution_assembler = video_creative_execution_assembler

    def create_video_creative_execution(self, video_creative_execution: VideoCreativeExecution) -> VideoCreativeExecutionDto:
        created = self.video_creative_execution_repository.create(video_creative_execution)
        return self.get_video_creative_execution_by_id(id=created.id)

    def get_video_creative_execution_by_id(self, id: int) -> VideoCreativeExecutionDto:
        video_creative_execution_db = self.video_creative_execution_repository.get_by_id(id)

        if not video_creative_execution_db:
            raise ValueError(f"Video creative execution {id} not found")

        video_creative_execution_dto = VideoCreativeExecutionMapper.to_dto(video_creative_execution_db)
        return self.video_creative_execution_assembler.assemble_dto(video_creative_execution_dto)

    def get_video_creative_executions_by_ad_execution(self, ad_execution_id: int) -> List[VideoCreativeExecutionDto]:
        items = self.video_creative_execution_repository.get_by_ad_execution_id(ad_execution_id)
        dtos = [VideoCreativeExecutionMapper.to_dto(item) for item in items]
        return [self.video_creative_execution_assembler.assemble_dto(dto) for dto in dtos]
