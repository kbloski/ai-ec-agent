from di.container import Container


def get_marketing_strategy_offer_strategies_handler(
    marketing_strategy_id: int,
):
    container = Container()

    offer_strategy_service = container.offer_strategy_service()

    return offer_strategy_service.get_offer_strategies_by_marketing_strategy(
        marketing_strategy_id=marketing_strategy_id
    )
