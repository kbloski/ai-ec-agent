from di.container import Container


def delete_knowledge_insight_handler(id: int):
    container = Container()
    knowledge_insights_repository = container.knowledge_insights_repository()

    deleted = knowledge_insights_repository.delete(id=id)

    return {"deleted": deleted}
