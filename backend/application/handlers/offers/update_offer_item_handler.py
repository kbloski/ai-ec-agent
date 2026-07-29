from typing import Any, Dict

from di.container import Container
from application.mappers.offer_item_mapper import OfferItemMapper

DENYLIST = {"id", "offer_id", "created_at", "updated_at"}


def update_offer_item_handler(id: int, fields: Dict[str, Any]):
    container = Container()
    offer_items_repository = container.offer_items_repository()

    item = offer_items_repository.get_by_id(id)

    for key, value in fields.items():
        if key not in DENYLIST:
            setattr(item, key, value)

    updated = offer_items_repository.update(item)
    return OfferItemMapper.to_dto(updated).to_dict()
