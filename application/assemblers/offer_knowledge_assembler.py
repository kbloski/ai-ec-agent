from application.dtos.knowledge.offer_knowledge_dto import OfferKnowledgeDto
from application.mappers.knowledge_insight_mapper import KnowledgeInsightMapper
from application.mappers.target_audience_mapper import TargetAudienceMapper
from infrastructure.logging.logger import Logger
from infrastructure.repositories.offers_knowledge_repository import OfferKnowledgeRepository
from infrastructure.repositories.knowledge_insights_repository import KnowledgeInsightsRepository
from infrastructure.repositories.target_audiences_repository import TargetAudiencesRepository

class OfferKnowledgeAssembler:
    def __init__(
        self,
        logger : Logger,
        offer_knowledge_repository : OfferKnowledgeRepository,
        knowledge_insights_repository : KnowledgeInsightsRepository,
        target_audiences_repository : TargetAudiencesRepository
    ):
        self.offer_knowledge_repository = offer_knowledge_repository
        self.knowledge_insights_repository = knowledge_insights_repository
        self.target_audiences_repository = target_audiences_repository

    def assemble_dto(self, item : OfferKnowledgeDto) -> OfferKnowledgeDto:
        offer_insights = self.knowledge_insights_repository.find_by_offer_id_or_knowledge_id(item.id)
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
    

