from infrastructure.logging.logger import Logger
from application.dtos.creative_strategy.creative_strategy_response_dto import CreativeStrategyDto


class CreativeStrategyAssembler:
    def __init__(self, logger: Logger):
        self.logger = logger

    def assemble_dto(self, item: CreativeStrategyDto) -> CreativeStrategyDto:
        return item
