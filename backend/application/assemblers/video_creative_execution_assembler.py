from infrastructure.logging.logger import Logger
from application.dtos.video_creative_execution.video_creative_execution_response_dto import VideoCreativeExecutionDto


class VideoCreativeExecutionAssembler:
    def __init__(self, logger: Logger):
        self.logger = logger

    def assemble_dto(self, item: VideoCreativeExecutionDto) -> VideoCreativeExecutionDto:
        return item
