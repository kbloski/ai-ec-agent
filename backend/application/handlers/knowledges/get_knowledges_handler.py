from di.container import Container
from application.mappers.knowledge_mapper import KnowledgeMapper


# =====================================================
# MAIN HANDLER
# =====================================================

def get_knowledges_handler(
    offer_id: int,
):
    container = Container()

    knowledge_repository = (
        container.knowledge_repository()
    )


    items = knowledge_repository.get_by_offer_id(
        offer_id
    )

    dtos = [
        KnowledgeMapper.to_dto(item)
        for item in items
    ]

    return dtos
