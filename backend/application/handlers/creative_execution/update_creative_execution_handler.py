from typing import Any, Dict

from di.container import Container
from application.mappers.creative_execution_mapper import CreativeExecutionMapper

DENYLIST = {"id", "ad_execution_id", "created_at", "updated_at"}


def update_creative_execution_handler(id: int, fields: Dict[str, Any]):
    container = Container()
    creative_execution_repository = container.creative_execution_repository()

    item = creative_execution_repository.get_by_id(id)

    for key, value in fields.items():
        if key not in DENYLIST:
            setattr(item, key, value)

    updated = creative_execution_repository.update(item)
    return CreativeExecutionMapper.to_dto(updated).to_dict()
