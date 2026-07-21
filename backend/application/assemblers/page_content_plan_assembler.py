from infrastructure.logging.logger import Logger
from application.dtos.page_content_plan.page_content_plan_response_dto import PageContentPlanDto


class PageContentPlanAssembler:
    def __init__(self, logger: Logger):
        self.logger = logger

    def assemble_dto(self, item: PageContentPlanDto) -> PageContentPlanDto:
        return item
