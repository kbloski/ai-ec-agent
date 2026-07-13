from domain.models.knowledge.offer_knowledge import OfferKnowledge
from application.dtos.knowledge.offer_knowledge_dto import OfferKnowledgeDto

class OfferKnowledgeMapper:

    @staticmethod
    def to_dto(item : OfferKnowledge) -> OfferKnowledgeDto:
        return OfferKnowledgeDto(
            id = item.id,
            offer_id = item.offer_id,
            version = item.version,
            content_status= item.content_status,
            offer_summary = item.offer_summary,
            category = item.category,
            value_proposition = item.value_proposition,
        )

