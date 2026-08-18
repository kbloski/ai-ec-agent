from infrastructure.logging.logger import Logger
from application.dtos.page_requirements.page_requirements_dto import PageRequirementsDto
from application.mappers.page_section_requirement_mapper import PageSectionRequirementMapper
from infrastructure.repositories.page_section_requirements_repository import PageSectionRequirementsRepository


class PageRequirementsAssembler:
    logger: Logger
    page_section_requirements_repository: PageSectionRequirementsRepository

    def __init__(
        self,
        logger: Logger,
        page_section_requirements_repository: PageSectionRequirementsRepository,
    ):
        self.logger = logger
        self.page_section_requirements_repository = page_section_requirements_repository

    def assemble_dto(self, item: PageRequirementsDto) -> PageRequirementsDto:
        section_requirements_db = self.page_section_requirements_repository.find_for_page_requirements(
            page_requirements_id=item.id
        )
        item.page_section_requirements = [
            PageSectionRequirementMapper.to_dto(item=i) for i in section_requirements_db
        ]

        return item
