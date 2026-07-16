from di.container import Container


def get_knowledge_experiment_handler(
    id: int,
):
    container = Container()

    experiment_service = container.experiment_service()

    return experiment_service.get_experiment_by_id(id=id)
