from typing import Any, Dict

from di.container import Container
from application.mappers.offer_knowledge_mapper import OfferKnowledgeMapper

DENYLIST = {"id", "offer_id", "created_at", "updated_at"}


def update_offer_knowledge_handler(id: int, fields: Dict[str, Any]):
    container = Container()
    offer_knowledge_repository = container.offer_knowledge_repository()
    offer_knowledge_assembler = container.offer_knowledge_assembler()

    item = offer_knowledge_repository.get_by_id(id)

    for key, value in fields.items():
        if key not in DENYLIST:
            setattr(item, key, value)

    updated = offer_knowledge_repository.update(item)
    dto = OfferKnowledgeMapper.to_dto(updated)
    return offer_knowledge_assembler.assemble_dto(dto)
