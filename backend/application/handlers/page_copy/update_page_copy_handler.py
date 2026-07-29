from typing import Any, Dict

from di.container import Container
from application.mappers.page_copy_mapper import PageCopyMapper

DENYLIST = {"id", "page_content_plan_id", "created_at", "updated_at"}


def update_page_copy_handler(id: int, fields: Dict[str, Any]):
    container = Container()
    page_copy_repository = container.page_copy_repository()

    item = page_copy_repository.get_by_id(id)

    for key, value in fields.items():
        if key not in DENYLIST:
            setattr(item, key, value)

    updated = page_copy_repository.update(item)
    return PageCopyMapper.to_dto(updated).to_dict()
