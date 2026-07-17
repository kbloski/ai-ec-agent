from di.container import Container


def get_creative_strategy_handler(
    id: int,
):
    container = Container()

    creative_strategy_service = container.creative_strategy_service()

    return creative_strategy_service.get_creative_strategy_by_id(id=id)
