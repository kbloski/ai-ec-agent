from application.dtos.knowledge.knowledge_dto import KnowledgeDto
from application.mappers.knowledge_insight_mapper import KnowledgeInsightMapper
from application.mappers.target_audience_mapper import TargetAudienceMapper
from infrastructure.logging.logger import Logger
from infrastructure.repositories.knowledge_repository import KnowledgeRepository
from infrastructure.repositories.knowledge_insights_repository import KnowledgeInsightsRepository
from infrastructure.repositories.target_audiences_repository import TargetAudiencesRepository

class KnowledgeAssembler:
    def __init__(
        self,
        logger : Logger,
        knowledge_repository : KnowledgeRepository,
        knowledge_insights_repository : KnowledgeInsightsRepository,
        target_audiences_repository : TargetAudiencesRepository
    ):
        self.knowledge_repository = knowledge_repository
        self.knowledge_insights_repository = knowledge_insights_repository
        self.target_audiences_repository = target_audiences_repository

    def assemble_dto(self, item : KnowledgeDto) -> KnowledgeDto:
        offer_insights = self.knowledge_insights_repository.find_by_knowledge_id(item.id)
        item.offer_insights = [
            KnowledgeInsightMapper.to_dto(i)
            for i in offer_insights
        ]

        # item
        target_audiences = self.target_audiences_repository.find_for_knowledge(knowledge_id=item.id)
        item.target_audiences = [
            TargetAudienceMapper.to_dto(t)
            for t in target_audiences
        ]

        return item


