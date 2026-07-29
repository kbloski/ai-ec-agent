from typing import Any, Dict

from di.container import Container
from application.mappers.ad_execution_mapper import AdExecutionMapper

DENYLIST = {"id", "creative_strategy_id", "created_at", "updated_at"}


def update_ad_execution_handler(id: int, fields: Dict[str, Any]):
    container = Container()
    ad_execution_repository = container.ad_execution_repository()

    item = ad_execution_repository.get_by_id(id)

    for key, value in fields.items():
        if key not in DENYLIST:
            setattr(item, key, value)

    updated = ad_execution_repository.update(item)
    return AdExecutionMapper.to_dto(updated).to_dict()
