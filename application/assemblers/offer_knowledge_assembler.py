from application.dtos.offers.offer_knowledge_dto import OfferKnowledgeDto
from application.mappers.offer_insight_mapper import OfferInsightsMapper
from infrastructure.logging.logger import Logger
from infrastructure.repositories.offers_knowledge_repository import OfferKnowledgeRepository
from infrastructure.repositories.offer_insights_repository import OfferInsightsRepository

class OfferKnowledgeAssembler:
    def __init__(
        self,
        logger : Logger,
        offer_knowledge_repository : OfferKnowledgeRepository,
        offer_insights_repository : OfferInsightsRepository 
    ):
        self.offer_knowledge_repository = offer_knowledge_repository
        self.offer_insights_repository = offer_insights_repository

    def assemble_dto(self, item : OfferKnowledgeDto) -> OfferKnowledgeDto:
        offer_items = self.offer_insights_repository.find_by_offer_id_or_knowledge_id(item.id)

        item.offer_items = [
            OfferInsightsMapper.to_dto(i)
            for i in offer_items
        ]
        
        return item
    

