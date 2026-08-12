from application.dtos.audience.target_audience_dto import TargetAudienceDto
from application.mappers.knowledge_insight_mapper import KnowledgeInsightMapper
from infrastructure.logging.logger import Logger
from infrastructure.repositories.knowledge_repository import KnowledgeRepository
from infrastructure.repositories.knowledge_insights_repository import KnowledgeInsightsRepository

class TargetAudienceAssembler:
    def __init__(
        self,
        logger : Logger
    ):
        self.logger=logger

    def assemble_dto(self, item : TargetAudienceDto) -> TargetAudienceDto:
        return item
    

