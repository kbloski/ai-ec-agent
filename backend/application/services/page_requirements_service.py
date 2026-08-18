import json

from typing import List

from infrastructure.logging.logger import Logger
from domain.models.page_requirements.page_requirements import PageRequirements
from domain.enums.context_section_purpose import ContextSectionPurpose
from application.dtos.page_requirements.page_requirements_dto import PageRequirementsDto
from infrastructure.repositories.page_requirements_repository import PageRequirementsRepository
from application.mappers.page_requirements_mapper import PageRequirementsMapper
from application.assemblers.page_requirements_assembler import PageRequirementsAssembler
from application.services.llm_context_builder import build_llm_section


class PageRequirementsService:

    def __init__(
        self,
        logger: Logger,
        page_requirements_repository: PageRequirementsRepository,
        page_requirements_assembler: PageRequirementsAssembler,
    ):
        self.logger = logger
        self.page_requirements_repository = page_requirements_repository
        self.page_requirements_assembler = page_requirements_assembler

    def create_page_requirements(self, page_requirements: PageRequirements) -> PageRequirementsDto:
        created = self.page_requirements_repository.create(page_requirements)
        return self.get_page_requirements_by_id(id=created.id)

    def get_page_requirements_by_id(self, id: int) -> PageRequirementsDto:
        page_requirements_db = self.page_requirements_repository.get_by_id(id)

        if not page_requirements_db:
            raise ValueError(f"Page requirements {id} not found")

        page_requirements_dto = PageRequirementsMapper.to_dto(page_requirements_db)
        return self.page_requirements_assembler.assemble_dto(page_requirements_dto)

    def get_page_requirements_by_page_strategy(self, page_strategy_id: int) -> List[PageRequirementsDto]:
        items = self.page_requirements_repository.get_by_page_strategy_id(page_strategy_id)
        dtos = [PageRequirementsMapper.to_dto(item) for item in items]
        return [self.page_requirements_assembler.assemble_dto(dto) for dto in dtos]

    def build_llm_context(self, page_requirements_id: int) -> str:
        page_requirements_json = json.dumps(
            self.get_page_requirements_by_id(id=page_requirements_id).to_content_dict(),
            ensure_ascii=False,
            indent=2,
            default=str
        )

        return build_llm_section(
            "page-requirements",
            page_requirements_json,
            purpose=ContextSectionPurpose.PAGE_REQUIREMENTS.value,
        )
