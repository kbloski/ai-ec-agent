from di.container import Container
from application.mappers.offer_insight_mapper import OfferInsightMapper


def get_offer_insight_handler(id: int):
    container = Container()
    offer_insights_repository = container.offer_insights_repository()

    item = offer_insights_repository.get_by_id(id)
    return OfferInsightMapper.to_dto(item).to_dict()
