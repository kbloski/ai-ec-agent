from di.container import Container
from application.mappers.offer_knowledge_mapper import OfferKnowledgeMapper


# =====================================================
# MAIN HANDLER
# =====================================================

def get_offer_knowledge_handler(
    offer_id: int,
    knowledge_id: int
):
    container = Container()

    offer_knowledge_repository = (
        container.offer_knowledge_repository()
    )

    offer_knowledge_assembler = (
        container.offer_knowledge_assembler()
    )


    item = offer_knowledge_repository.get_by_id(
        knowledge_id
    )

    if not item:
        raise ValueError(
            f"Offer knowledge {knowledge_id} not found"
        )


    item_dto = OfferKnowledgeMapper.to_dto(
        item
    )


    result = offer_knowledge_assembler.assemble_dto(
        item_dto
    )


    return result