from typing import Any, Dict

from di.container import Container
from application.mappers.offer_strategy_mapper import OfferStrategyMapper

DENYLIST = {"id", "marketing_strategy_id", "created_at", "updated_at"}


def update_offer_strategy_handler(id: int, fields: Dict[str, Any]):
    container = Container()
    offer_strategy_repository = container.offer_strategy_repository()

    item = offer_strategy_repository.get_by_id(id)

    for key, value in fields.items():
        if key not in DENYLIST:
            setattr(item, key, value)

    updated = offer_strategy_repository.update(item)
    return OfferStrategyMapper.to_dto(updated).to_dict()
