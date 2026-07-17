from di.container import Container


def get_offer_strategy_handler(
    id: int,
):
    container = Container()

    offer_strategy_service = container.offer_strategy_service()

    return offer_strategy_service.get_offer_strategy_by_id(id=id)
