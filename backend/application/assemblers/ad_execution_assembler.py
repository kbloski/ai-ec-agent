from infrastructure.logging.logger import Logger
from application.dtos.ad_execution.ad_execution_response_dto import AdExecutionDto


class AdExecutionAssembler:
    def __init__(self, logger: Logger):
        self.logger = logger

    def assemble_dto(self, item: AdExecutionDto) -> AdExecutionDto:
        return item
