from domain.models.offers.offer_insight import OfferInsight
from application.dtos.offers.offer_insight_dto import OfferInsightDto

class OfferInsightsMapper:

    @staticmethod
    def to_dto(item : OfferInsight) -> OfferInsightDto:
        return OfferInsightDto(
            id = item.id,
            offer_id = item.offer_id,
            knowledge_id = item.knowledge_id,
            type = item.type,
            status = item.status,
            value = item.value,
        )

