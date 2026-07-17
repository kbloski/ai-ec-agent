from di.container import Container


def get_offer_strategy_message_strategies_handler(
    offer_strategy_id: int,
):
    container = Container()

    message_strategy_service = container.message_strategy_service()

    return message_strategy_service.get_message_strategies_by_offer_strategy(
        offer_strategy_id=offer_strategy_id
    )
