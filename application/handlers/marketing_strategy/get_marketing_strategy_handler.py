from di.container import Container


def get_marketing_strategy_handler(
    id: int,
):
    container = Container()

    marketing_strategy_service = container.marketing_strategy_service()

    return marketing_strategy_service.get_marketing_strategy_by_id(id=id)
