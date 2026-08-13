from domain.models.offers.offer_insight import OfferInsight
from application.dtos.offers.offer_insight_dto import OfferInsightDto

class OfferInsightMapper:

    @staticmethod
    def to_dto(item : OfferInsight) -> OfferInsightDto:
        return OfferInsightDto(
            id = item.id,
            offer_id = item.offer_id,
            type = item.type,
            fact_status = item.fact_status,
            review_status = item.review_status,
            value = item.value,
        )

