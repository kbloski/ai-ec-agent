from infrastructure.logging.logger import Logger
from application.dtos.creative_execution.creative_execution_response_dto import CreativeExecutionDto


class CreativeExecutionAssembler:
    def __init__(self, logger: Logger):
        self.logger = logger

    def assemble_dto(self, item: CreativeExecutionDto) -> CreativeExecutionDto:
        return item
