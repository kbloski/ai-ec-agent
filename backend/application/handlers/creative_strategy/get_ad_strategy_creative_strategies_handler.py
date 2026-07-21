from di.container import Container


def get_ad_strategy_creative_strategies_handler(
    ad_strategy_id: int,
):
    container = Container()

    creative_strategy_service = container.creative_strategy_service()

    return creative_strategy_service.get_creative_strategies_by_ad_strategy(
        ad_strategy_id=ad_strategy_id
    )
