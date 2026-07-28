import json
from typing import List

from infrastructure.logging.logger import Logger
from infrastructure.services.path_service import PathService


class AdFrameworksRepository:
    def __init__(self, logger: Logger, path_service: PathService):
        self.logger = logger
        self.path_service = path_service

    def get_all(self) -> List[dict]:
        with open(self.path_service.AD_FRAMEWORKS_FILE, "r", encoding="utf-8") as file:
            return json.load(file)
