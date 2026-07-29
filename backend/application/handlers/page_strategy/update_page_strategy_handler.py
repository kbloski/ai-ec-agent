from typing import Any, Dict

from di.container import Container
from application.mappers.page_strategy_mapper import PageStrategyMapper

DENYLIST = {"id", "message_strategy_id", "created_at", "updated_at"}


def update_page_strategy_handler(id: int, fields: Dict[str, Any]):
    container = Container()
    page_strategy_repository = container.page_strategy_repository()

    item = page_strategy_repository.get_by_id(id)

    for key, value in fields.items():
        if key not in DENYLIST:
            setattr(item, key, value)

    updated = page_strategy_repository.update(item)
    return PageStrategyMapper.to_dto(updated).to_dict()
