from di.container import Container
from application.mappers.knowledge_mapper import KnowledgeMapper


# =====================================================
# MAIN HANDLER
# =====================================================

def get_knowledge_handler(
    knowledge_id: int
):
    container = Container()

    knowledge_repository = (
        container.knowledge_repository()
    )

    knowledge_assembler = (
        container.knowledge_assembler()
    )


    item = knowledge_repository.get_by_id(
        knowledge_id
    )

    if not item:
        raise ValueError(
            f"Knowledge {knowledge_id} not found"
        )


    item_dto = KnowledgeMapper.to_dto(
        item
    )


    result = knowledge_assembler.assemble_dto(
        item_dto
    )


    return result
