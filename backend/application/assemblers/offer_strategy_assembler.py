from infrastructure.logging.logger import Logger
from application.dtos.offer_strategy.offer_strategy_response_dto import OfferStrategyDto


class OfferStrategyAssembler:
    def __init__(self, logger: Logger):
        self.logger = logger

    def assemble_dto(self, item: OfferStrategyDto) -> OfferStrategyDto:
        return item
