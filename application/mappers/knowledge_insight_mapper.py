from domain.models.knowledge.knowledge_insight import KnowledgeInsight
from application.dtos.knowledge.knowledge_insight_dto import KnowledgeInsightDto

class KnowledgeInsightMapper:

    @staticmethod
    def to_dto(item : KnowledgeInsight) -> KnowledgeInsightDto:
        return KnowledgeInsightDto(
            id = item.id,
            offer_id = item.offer_id,
            knowledge_id = item.knowledge_id,
            type = item.type,
            content_status = item.content_status,
            value = item.value,
        )

