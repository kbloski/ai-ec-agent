from typing import Any, Dict

from di.container import Container
from application.mappers.creative_strategy_mapper import CreativeStrategyMapper

DENYLIST = {"id", "ad_strategy_id", "created_at", "updated_at"}


def update_creative_strategy_handler(id: int, fields: Dict[str, Any]):
    container = Container()
    creative_strategy_repository = container.creative_strategy_repository()

    item = creative_strategy_repository.get_by_id(id)

    for key, value in fields.items():
        if key not in DENYLIST:
            setattr(item, key, value)

    updated = creative_strategy_repository.update(item)
    return CreativeStrategyMapper.to_dto(updated).to_dict()
