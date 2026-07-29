from typing import Any, Dict

from di.container import Container
from application.mappers.page_blueprint_mapper import PageBlueprintMapper

DENYLIST = {"id", "page_strategy_id", "created_at", "updated_at"}


def update_page_blueprint_handler(id: int, fields: Dict[str, Any]):
    container = Container()
    page_blueprint_repository = container.page_blueprint_repository()

    item = page_blueprint_repository.get_by_id(id)

    for key, value in fields.items():
        if key not in DENYLIST:
            setattr(item, key, value)

    updated = page_blueprint_repository.update(item)
    return PageBlueprintMapper.to_dto(updated).to_dict()
