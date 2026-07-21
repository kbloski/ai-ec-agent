from typing import List

from infrastructure.logging.logger import Logger
from domain.models.page_content_plan.page_content_plan import PageContentPlan
from application.dtos.page_content_plan.page_content_plan_response_dto import PageContentPlanDto
from infrastructure.repositories.page_content_plan_repository import PageContentPlanRepository
from application.mappers.page_content_plan_mapper import PageContentPlanMapper
from application.assemblers.page_content_plan_assembler import PageContentPlanAssembler


class PageContentPlanService:

    def __init__(
        self,
        logger: Logger,
        page_content_plan_repository: PageContentPlanRepository,
        page_content_plan_assembler: PageContentPlanAssembler,
    ):
        self.logger = logger
        self.page_content_plan_repository = page_content_plan_repository
        self.page_content_plan_assembler = page_content_plan_assembler

    def create_page_content_plan(self, page_content_plan: PageContentPlan) -> PageContentPlanDto:
        created = self.page_content_plan_repository.create(page_content_plan)
        return self.get_page_content_plan_by_id(id=created.id)

    def get_page_content_plan_by_id(self, id: int) -> PageContentPlanDto:
        page_content_plan_db = self.page_content_plan_repository.get_by_id(id)

        if not page_content_plan_db:
            raise ValueError(f"Page content plan {id} not found")

        page_content_plan_dto = PageContentPlanMapper.to_dto(page_content_plan_db)
        return self.page_content_plan_assembler.assemble_dto(page_content_plan_dto)

    def get_page_content_plans_by_page_blueprint(self, page_blueprint_id: int) -> List[PageContentPlanDto]:
        items = self.page_content_plan_repository.get_by_page_blueprint_id(page_blueprint_id)
        dtos = [PageContentPlanMapper.to_dto(item) for item in items]
        return [self.page_content_plan_assembler.assemble_dto(dto) for dto in dtos]
