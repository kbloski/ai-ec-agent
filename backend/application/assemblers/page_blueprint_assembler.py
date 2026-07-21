from infrastructure.logging.logger import Logger
from application.dtos.page_blueprint.page_blueprint_response_dto import PageBlueprintDto


class PageBlueprintAssembler:
    def __init__(self, logger: Logger):
        self.logger = logger

    def assemble_dto(self, item: PageBlueprintDto) -> PageBlueprintDto:
        return item
