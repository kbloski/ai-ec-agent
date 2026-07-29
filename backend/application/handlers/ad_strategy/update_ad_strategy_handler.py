from typing import Any, Dict

from di.container import Container
from application.mappers.ad_strategy_mapper import AdStrategyMapper

DENYLIST = {"id", "message_strategy_id", "created_at", "updated_at"}


def update_ad_strategy_handler(id: int, fields: Dict[str, Any]):
    container = Container()
    ad_strategy_repository = container.ad_strategy_repository()

    item = ad_strategy_repository.get_by_id(id)

    for key, value in fields.items():
        if key not in DENYLIST:
            setattr(item, key, value)

    updated = ad_strategy_repository.update(item)
    return AdStrategyMapper.to_dto(updated).to_dict()
