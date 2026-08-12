import json

from infrastructure.logging.logger import Logger
from infrastructure.repositories.platforms_repository import PlatformsRepository
from application.services.llm_context_builder import build_llm_section
from domain.enums.context_section_purpose import ContextSectionPurpose


class PlatformService:

    def __init__(self, logger: Logger, platforms_repository: PlatformsRepository):
        self.logger = logger
        self.platforms_repository = platforms_repository

    def build_llm_context(self, platform_id: str) -> str | None:
        platform = self.platforms_repository.get_by_id(platform_id)

        if platform is None:
            return None

        platform_json = json.dumps(platform, ensure_ascii=False, indent=2, default=str)

        return build_llm_section("platform", platform_json, purpose=ContextSectionPurpose.PLATFORM.value)
