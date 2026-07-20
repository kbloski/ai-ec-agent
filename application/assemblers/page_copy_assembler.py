from infrastructure.logging.logger import Logger
from application.dtos.page_copy.page_copy_response_dto import PageCopyDto


class PageCopyAssembler:
    def __init__(self, logger: Logger):
        self.logger = logger

    def assemble_dto(self, item: PageCopyDto) -> PageCopyDto:
        return item
