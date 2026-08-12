from typing import Any, Dict

from di.container import Container
from application.mappers.knowledge_mapper import KnowledgeMapper

DENYLIST = {"id", "offer_id", "created_at", "updated_at"}


def update_knowledge_handler(id: int, fields: Dict[str, Any]):
    container = Container()
    knowledge_repository = container.knowledge_repository()
    knowledge_assembler = container.knowledge_assembler()

    item = knowledge_repository.get_by_id(id)

    for key, value in fields.items():
        if key not in DENYLIST:
            setattr(item, key, value)

    updated = knowledge_repository.update(item)
    dto = KnowledgeMapper.to_dto(updated)
    return knowledge_assembler.assemble_dto(dto)
