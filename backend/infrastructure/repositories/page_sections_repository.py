import json
from typing import List, Optional

from infrastructure.logging.logger import Logger
from infrastructure.services.path_service import PathService


class PageSectionsRepository:
    def __init__(self, logger: Logger, path_service: PathService):
        self.logger = logger
        self.path_service = path_service

    def get_all(self) -> List[dict]:
        with open(self.path_service.PAGE_SECTION_TYPES_FILE, "r", encoding="utf-8") as file:
            return json.load(file)

    def get_by_id(self, section_type_id: str) -> Optional[dict]:
        for section_type in self.get_all():
            if section_type.get("id") == section_type_id:
                return section_type
        return None
