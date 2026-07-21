from di.container import Container


def get_message_strategy_ad_strategies_handler(
    message_strategy_id: int,
):
    container = Container()

    ad_strategy_service = container.ad_strategy_service()

    return ad_strategy_service.get_ad_strategies_by_message_strategy(
        message_strategy_id=message_strategy_id
    )
