from domain.models.knowledge.knowledge_insight import KnowledgeInsight
from application.dtos.knowledge.knowledge_insight_dto import KnowledgeInsightDto

class KnowledgeInsightMapper:

    @staticmethod
    def to_dto(item : KnowledgeInsight) -> KnowledgeInsightDto:
        return KnowledgeInsightDto(
            id = item.id,
            knowledge_id = item.knowledge_id,
            type = item.type,
            fact_status = item.fact_status,
            review_status = item.review_status,
            value = item.value,
        )

