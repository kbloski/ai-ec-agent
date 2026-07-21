from di.container import Container


def get_message_strategy_page_strategies_handler(
    message_strategy_id: int,
):
    container = Container()

    page_strategy_service = container.page_strategy_service()

    return page_strategy_service.get_page_strategies_by_message_strategy(
        message_strategy_id=message_strategy_id
    )
