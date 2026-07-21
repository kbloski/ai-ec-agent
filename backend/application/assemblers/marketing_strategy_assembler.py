from infrastructure.logging.logger import Logger
from application.dtos.marketing_strategy.marketing_strategy_response_dto import MarketingStrategyDto


class MarketingStrategyAssembler:
    def __init__(self, logger: Logger):
        self.logger = logger

    def assemble_dto(self, item: MarketingStrategyDto) -> MarketingStrategyDto:
        return item
