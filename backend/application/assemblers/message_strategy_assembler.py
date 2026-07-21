from infrastructure.logging.logger import Logger
from application.dtos.message_strategy.message_strategy_response_dto import MessageStrategyDto


class MessageStrategyAssembler:
    def __init__(self, logger: Logger):
        self.logger = logger

    def assemble_dto(self, item: MessageStrategyDto) -> MessageStrategyDto:
        return item
