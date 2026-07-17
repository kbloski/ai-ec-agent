from di.container import Container


def get_ad_strategy_handler(
    id: int,
):
    container = Container()

    ad_strategy_service = container.ad_strategy_service()

    return ad_strategy_service.get_ad_strategy_by_id(id=id)
