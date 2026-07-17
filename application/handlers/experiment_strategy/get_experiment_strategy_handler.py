from di.container import Container


def get_experiment_strategy_handler(
    id: int,
):
    container = Container()

    experiment_strategy_service = container.experiment_strategy_service()

    return experiment_strategy_service.get_experiment_strategy_by_id(id=id)
