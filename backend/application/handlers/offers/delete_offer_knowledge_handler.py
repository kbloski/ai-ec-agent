from di.container import Container


def delete_offer_knowledge_handler(id: int):
    container = Container()
    offer_knowledge_repository = container.offer_knowledge_repository()

    deleted = offer_knowledge_repository.delete(id=id)

    return {"deleted": deleted}
