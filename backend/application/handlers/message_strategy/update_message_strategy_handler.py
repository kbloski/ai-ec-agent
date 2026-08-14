from typing import Any, Dict

from di.container import Container
from application.mappers.message_strategy_mapper import MessageStrategyMapper

DENYLIST = {"id", "offer_strategy_id", "created_at", "updated_at"}


def update_message_strategy_handler(id: int, fields: Dict[str, Any]):
    container = Container()
    message_strategy_repository = container.message_strategy_repository()

    item = message_strategy_repository.get_by_id(id)

    for key, value in fields.items():
        if key not in DENYLIST:
            setattr(item, key, value)

    updated = message_strategy_repository.update(item)
    return MessageStrategyMapper.to_dto(updated).to_dict()
