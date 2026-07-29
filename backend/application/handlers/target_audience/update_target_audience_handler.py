from typing import Any, Dict
from di.container import Container
from application.mappers.target_audience_mapper import TargetAudienceMapper


def update_target_audience_handler(id: int, fields: Dict[str, Any]):
    container = Container()
    repo = container.target_audiences_repository()
    assembler = container.target_audience_assembler()

    item = repo.find_by_id(id)

    for key, value in fields.items():
        if value is not None:
            setattr(item, key, value)

    updated = repo.update(item)

    dto = TargetAudienceMapper.to_dto(updated)
    return assembler.assemble_dto(dto)
