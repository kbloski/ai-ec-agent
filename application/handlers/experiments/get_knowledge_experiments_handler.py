from di.container import Container


def get_knowledge_experiments_handler(
    knowledge_id: int,
):
    container = Container()

    experiment_service = container.experiment_service()

    return experiment_service.get_experiments_by_knowledge(knowledge_id=knowledge_id)
