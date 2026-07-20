from di.container import Container


def get_offer_strategy_page_strategies_handler(
    offer_strategy_id: int,
):
    container = Container()

    page_strategy_service = container.page_strategy_service()

    return page_strategy_service.get_page_strategies_by_offer_strategy(
        offer_strategy_id=offer_strategy_id
    )
