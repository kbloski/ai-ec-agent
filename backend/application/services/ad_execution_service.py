from typing import List

from infrastructure.logging.logger import Logger
from domain.models.ad_execution.ad_execution import AdExecution
from application.dtos.ad_execution.ad_execution_response_dto import AdExecutionDto
from infrastructure.repositories.ad_execution_repository import AdExecutionRepository
from application.mappers.ad_execution_mapper import AdExecutionMapper
from application.assemblers.ad_execution_assembler import AdExecutionAssembler


class AdExecutionService:

    def __init__(
        self,
        logger: Logger,
        ad_execution_repository: AdExecutionRepository,
        ad_execution_assembler: AdExecutionAssembler,
    ):
        self.logger = logger
        self.ad_execution_repository = ad_execution_repository
        self.ad_execution_assembler = ad_execution_assembler

    def create_ad_execution(self, ad_execution: AdExecution) -> AdExecutionDto:
        created = self.ad_execution_repository.create(ad_execution)
        return self.get_ad_execution_by_id(id=created.id)

    def get_ad_execution_by_id(self, id: int) -> AdExecutionDto:
        ad_execution_db = self.ad_execution_repository.get_by_id(id)

        if not ad_execution_db:
            raise ValueError(f"Ad execution {id} not found")

        ad_execution_dto = AdExecutionMapper.to_dto(ad_execution_db)
        return self.ad_execution_assembler.assemble_dto(ad_execution_dto)

    def get_ad_executions_by_creative_strategy(self, creative_strategy_id: int) -> List[AdExecutionDto]:
        items = self.ad_execution_repository.get_by_creative_strategy_id(creative_strategy_id)
        dtos = [AdExecutionMapper.to_dto(item) for item in items]
        return [self.ad_execution_assembler.assemble_dto(dto) for dto in dtos]
