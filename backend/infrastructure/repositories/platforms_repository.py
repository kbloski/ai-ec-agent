import json
from typing import List, Optional

from infrastructure.logging.logger import Logger
from infrastructure.services.path_service import PathService


class PlatformsRepository:
    def __init__(self, logger: Logger, path_service: PathService):
        self.logger = logger
        self.path_service = path_service

    def get_all(self) -> List[dict]:
        with open(self.path_service.PLATFORMS_FILE, "r", encoding="utf-8") as file:
            return json.load(file)

    def get_by_id(self, platform_id: str) -> Optional[dict]:
        for platform in self.get_all():
            if platform.get("id") == platform_id:
                return platform
        return None
