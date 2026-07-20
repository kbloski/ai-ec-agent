from typing import List

from infrastructure.logging.logger import Logger
from domain.models.page_strategy.page_strategy import PageStrategy
from application.dtos.page_strategy.page_strategy_response_dto import PageStrategyDto
from infrastructure.repositories.page_strategy_repository import PageStrategyRepository
from application.mappers.page_strategy_mapper import PageStrategyMapper
from application.assemblers.page_strategy_assembler import PageStrategyAssembler


class PageStrategyService:

    def __init__(
        self,
        logger: Logger,
        page_strategy_repository: PageStrategyRepository,
        page_strategy_assembler: PageStrategyAssembler,
    ):
        self.logger = logger
        self.page_strategy_repository = page_strategy_repository
        self.page_strategy_assembler = page_strategy_assembler

    def create_page_strategy(self, page_strategy: PageStrategy) -> PageStrategyDto:
        created = self.page_strategy_repository.create(page_strategy)
        return self.get_page_strategy_by_id(id=created.id)

    def get_page_strategy_by_id(self, id: int) -> PageStrategyDto:
        page_strategy_db = self.page_strategy_repository.get_by_id(id)

        if not page_strategy_db:
            raise ValueError(f"Page strategy {id} not found")

        page_strategy_dto = PageStrategyMapper.to_dto(page_strategy_db)
        return self.page_strategy_assembler.assemble_dto(page_strategy_dto)

    def get_page_strategies_by_offer_strategy(self, offer_strategy_id: int) -> List[PageStrategyDto]:
        items = self.page_strategy_repository.get_by_offer_strategy_id(offer_strategy_id)
        dtos = [PageStrategyMapper.to_dto(item) for item in items]
        return [self.page_strategy_assembler.assemble_dto(dto) for dto in dtos]
