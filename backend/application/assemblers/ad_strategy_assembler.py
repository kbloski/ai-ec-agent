from infrastructure.logging.logger import Logger
from application.dtos.ad_strategy.ad_strategy_response_dto import AdStrategyDto


class AdStrategyAssembler:
    def __init__(self, logger: Logger):
        self.logger = logger

    def assemble_dto(self, item: AdStrategyDto) -> AdStrategyDto:
        return item
