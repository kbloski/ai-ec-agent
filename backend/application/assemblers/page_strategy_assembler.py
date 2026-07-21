from infrastructure.logging.logger import Logger
from application.dtos.page_strategy.page_strategy_response_dto import PageStrategyDto


class PageStrategyAssembler:
    def __init__(self, logger: Logger):
        self.logger = logger

    def assemble_dto(self, item: PageStrategyDto) -> PageStrategyDto:
        return item
