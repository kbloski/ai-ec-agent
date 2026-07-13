from di.container import Container
from application.mappers.offer_knowledge_mapper import OfferKnowledgeMapper


# =====================================================
# MAIN HANDLER
# =====================================================

def get_offer_knowledges_handler(
    offer_id: int,
):
    container = Container()

    offer_knowledge_repository = (
        container.offer_knowledge_repository()
    )


    items = offer_knowledge_repository.get_by_offer_id(
        offer_id
    )

    dtos = [
        OfferKnowledgeMapper.to_dto(item)
        for item in items
    ]

    return dtos