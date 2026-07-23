from typing import List

from infrastructure.logging.logger import Logger
from domain.models.creative_execution.creative_execution import CreativeExecution
from application.dtos.creative_execution.creative_execution_response_dto import CreativeExecutionDto
from infrastructure.repositories.creative_execution_repository import CreativeExecutionRepository
from application.mappers.creative_execution_mapper import CreativeExecutionMapper
from application.assemblers.creative_execution_assembler import CreativeExecutionAssembler


class CreativeExecutionService:

    def __init__(
        self,
        logger: Logger,
        creative_execution_repository: CreativeExecutionRepository,
        creative_execution_assembler: CreativeExecutionAssembler,
    ):
        self.logger = logger
        self.creative_execution_repository = creative_execution_repository
        self.creative_execution_assembler = creative_execution_assembler

    def create_creative_execution(self, creative_execution: CreativeExecution) -> CreativeExecutionDto:
        created = self.creative_execution_repository.create(creative_execution)
        return self.get_creative_execution_by_id(id=created.id)

    def get_creative_execution_by_id(self, id: int) -> CreativeExecutionDto:
        creative_execution_db = self.creative_execution_repository.get_by_id(id)

        if not creative_execution_db:
            raise ValueError(f"Creative execution {id} not found")

        creative_execution_dto = CreativeExecutionMapper.to_dto(creative_execution_db)
        return self.creative_execution_assembler.assemble_dto(creative_execution_dto)

    def get_creative_executions_by_ad_execution(self, ad_execution_id: int) -> List[CreativeExecutionDto]:
        items = self.creative_execution_repository.get_by_ad_execution_id(ad_execution_id)
        dtos = [CreativeExecutionMapper.to_dto(item) for item in items]
        return [self.creative_execution_assembler.assemble_dto(dto) for dto in dtos]
