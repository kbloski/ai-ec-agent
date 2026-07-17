from typing import List

from infrastructure.logging.logger import Logger
from domain.models.creative_strategy.creative_strategy import CreativeStrategy
from application.dtos.creative_strategy.creative_strategy_response_dto import CreativeStrategyDto
from infrastructure.repositories.creative_strategy_repository import CreativeStrategyRepository
from application.mappers.creative_strategy_mapper import CreativeStrategyMapper
from application.assemblers.creative_strategy_assembler import CreativeStrategyAssembler


class CreativeStrategyService:

    def __init__(
        self,
        logger: Logger,
        creative_strategy_repository: CreativeStrategyRepository,
        creative_strategy_assembler: CreativeStrategyAssembler,
    ):
        self.logger = logger
        self.creative_strategy_repository = creative_strategy_repository
        self.creative_strategy_assembler = creative_strategy_assembler

    def create_creative_strategy(self, creative_strategy: CreativeStrategy) -> CreativeStrategyDto:
        created = self.creative_strategy_repository.create(creative_strategy)
        return self.get_creative_strategy_by_id(id=created.id)

    def get_creative_strategy_by_id(self, id: int) -> CreativeStrategyDto:
        creative_strategy_db = self.creative_strategy_repository.get_by_id(id)

        if not creative_strategy_db:
            raise ValueError(f"Creative strategy {id} not found")

        creative_strategy_dto = CreativeStrategyMapper.to_dto(creative_strategy_db)
        return self.creative_strategy_assembler.assemble_dto(creative_strategy_dto)

    def get_creative_strategies_by_ad_strategy(self, ad_strategy_id: int) -> List[CreativeStrategyDto]:
        items = self.creative_strategy_repository.get_by_ad_strategy_id(ad_strategy_id)
        dtos = [CreativeStrategyMapper.to_dto(item) for item in items]
        return [self.creative_strategy_assembler.assemble_dto(dto) for dto in dtos]
