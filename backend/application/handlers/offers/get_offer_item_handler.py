from di.container import Container
from application.mappers.offer_item_mapper import OfferItemMapper


def get_offer_item_handler(id: int):
    container = Container()
    offer_items_repository = container.offer_items_repository()

    item = offer_items_repository.get_by_id(id)
    return OfferItemMapper.to_dto(item).to_dict()
