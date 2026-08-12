from di.container import Container


def delete_knowledge_handler(id: int):
    container = Container()
    knowledge_repository = container.knowledge_repository()

    deleted = knowledge_repository.delete(id=id)

    return {"deleted": deleted}
