from typing import List

from infrastructure.logging.logger import Logger
from domain.models.message_strategy.message_strategy import MessageStrategy
from application.dtos.message_strategy.message_strategy_response_dto import MessageStrategyDto
from infrastructure.repositories.message_strategy_repository import MessageStrategyRepository
from application.mappers.message_strategy_mapper import MessageStrategyMapper
from application.assemblers.message_strategy_assembler import MessageStrategyAssembler


class MessageStrategyService:

    def __init__(
        self,
        logger: Logger,
        message_strategy_repository: MessageStrategyRepository,
        message_strategy_assembler: MessageStrategyAssembler,
    ):
        self.logger = logger
        self.message_strategy_repository = message_strategy_repository
        self.message_strategy_assembler = message_strategy_assembler

    def create_message_strategy(self, message_strategy: MessageStrategy) -> MessageStrategyDto:
        created = self.message_strategy_repository.create(message_strategy)
        return self.get_message_strategy_by_id(id=created.id)

    def get_message_strategy_by_id(self, id: int) -> MessageStrategyDto:
        message_strategy_db = self.message_strategy_repository.get_by_id(id)

        if not message_strategy_db:
            raise ValueError(f"Message strategy {id} not found")

        message_strategy_dto = MessageStrategyMapper.to_dto(message_strategy_db)
        return self.message_strategy_assembler.assemble_dto(message_strategy_dto)

    def get_message_strategies_by_offer_strategy(self, offer_strategy_id: int) -> List[MessageStrategyDto]:
        items = self.message_strategy_repository.get_by_offer_strategy_id(offer_strategy_id)
        dtos = [MessageStrategyMapper.to_dto(item) for item in items]
        return [self.message_strategy_assembler.assemble_dto(dto) for dto in dtos]
