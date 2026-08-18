from typing import List, Set

from infrastructure.logging.logger import Logger
from infrastructure.repositories.page_sections_repository import PageSectionsRepository


class PageSectionsService:
    def __init__(self, logger: Logger, page_sections_repository: PageSectionsRepository):
        self.logger = logger
        self.page_sections_repository = page_sections_repository

    def get_all(self) -> List[dict]:
        return self.page_sections_repository.get_all()

    def get_allowed_ids(self) -> Set[str]:
        return {section["id"] for section in self.get_all()}
