from di.container import Container
from application.mappers.offer_insight_mapper import OfferInsightMapper
from domain.enums.fact_status import FactStatus
from domain.enums.review_status import ReviewStatus


def update_offer_insight_handler(
    id: int,
    fact_status: str | None = None,
    review_status: str | None = None,
):
    container = Container()
    offer_insights_repository = container.offer_insights_repository()

    item = offer_insights_repository.get_by_id(id)
    if item is None:
        raise ValueError(f"Offer insight {id} not found")
    if fact_status is not None:
        item.fact_status = FactStatus(fact_status).value
    if review_status is not None:
        item.review_status = ReviewStatus(review_status).value

    updated = offer_insights_repository.update(item)
    return OfferInsightMapper.to_dto(updated).to_dict()
