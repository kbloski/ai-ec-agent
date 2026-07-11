from application.dtos.knowledge.offer_knowledge_dto import OfferKnowledgeDto
from application.mappers.knowledge_insight_mapper import KnowledgeInsightMapper
from infrastructure.logging.logger import Logger
from infrastructure.repositories.offers_knowledge_repository import OfferKnowledgeRepository
from infrastructure.repositories.knowledge_insights_repository import KnowledgeInsightsRepository

class OfferKnowledgeAssembler:
    def __init__(
        self,
        logger : Logger,
        offer_knowledge_repository : OfferKnowledgeRepository,
        knowledge_insights_repository : KnowledgeInsightsRepository 
    ):
        self.offer_knowledge_repository = offer_knowledge_repository
        self.knowledge_insights_repository = knowledge_insights_repository

    def assemble_dto(self, item : OfferKnowledgeDto) -> OfferKnowledgeDto:
        offer_items = self.knowledge_insights_repository.find_by_offer_id_or_knowledge_id(item.id)

        item.offer_items = [
            KnowledgeInsightMapper.to_dto(i)
            for i in offer_items
        ]
        
        return item
    

