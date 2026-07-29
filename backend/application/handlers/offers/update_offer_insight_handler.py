from di.container import Container
from application.mappers.offer_insight_mapper import OfferInsightMapper


def update_offer_insight_handler(id: int, content_status: str):
    container = Container()
    offer_insights_repository = container.offer_insights_repository()

    item = offer_insights_repository.get_by_id(id)
    item.content_status = content_status

    updated = offer_insights_repository.update(item)
    return OfferInsightMapper.to_dto(updated).to_dict()
