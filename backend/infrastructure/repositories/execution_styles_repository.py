import json
from typing import List, Optional

from infrastructure.logging.logger import Logger
from infrastructure.services.path_service import PathService


class ExecutionStylesRepository:
    def __init__(self, logger: Logger, path_service: PathService):
        self.logger = logger
        self.path_service = path_service

    def get_all(self) -> List[dict]:
        with open(self.path_service.EXECUTION_STYLES_FILE, "r", encoding="utf-8") as file:
            return json.load(file)

    def get_by_id(self, execution_style_id: str) -> Optional[dict]:
        for execution_style in self.get_all():
            if execution_style.get("id") == execution_style_id:
                return execution_style
        return None
