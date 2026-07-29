from typing import Any, Dict

from di.container import Container
from application.mappers.offer_mapper import OfferMapper

DENYLIST = {"id", "created_at", "updated_at"}


def update_offer_handler(id: int, fields: Dict[str, Any]):
    container = Container()
    offers_repository = container.offers_repository()
    offer_assembler = container.offer_assembler()

    item = offers_repository.get_by_id(id)

    for key, value in fields.items():
        if key not in DENYLIST:
            setattr(item, key, value)

    updated = offers_repository.update(item)
    dto = OfferMapper.to_dto(updated)
    return offer_assembler.assemble_dto(dto)
