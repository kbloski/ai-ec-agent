from domain.models.knowledge.knowledge import Knowledge
from application.dtos.knowledge.knowledge_dto import KnowledgeDto

class KnowledgeMapper:

    @staticmethod
    def to_dto(item : Knowledge) -> KnowledgeDto:
        return KnowledgeDto(
            id = item.id,
            offer_id = item.offer_id,
            offer_summary = item.offer_summary,
            category = item.category,
            value_proposition = item.value_proposition,
        )
