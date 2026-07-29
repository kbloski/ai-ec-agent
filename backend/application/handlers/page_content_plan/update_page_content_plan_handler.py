from typing import Any, Dict

from di.container import Container
from application.mappers.page_content_plan_mapper import PageContentPlanMapper

DENYLIST = {"id", "page_blueprint_id", "created_at", "updated_at"}


def update_page_content_plan_handler(id: int, fields: Dict[str, Any]):
    container = Container()
    page_content_plan_repository = container.page_content_plan_repository()

    item = page_content_plan_repository.get_by_id(id)

    for key, value in fields.items():
        if key not in DENYLIST:
            setattr(item, key, value)

    updated = page_content_plan_repository.update(item)
    return PageContentPlanMapper.to_dto(updated).to_dict()
