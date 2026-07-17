from di.container import Container


def get_brand_marketing_marketing_strategies_handler(
    brand_marketing_id: int,
):
    container = Container()

    marketing_strategy_service = container.marketing_strategy_service()

    return marketing_strategy_service.get_marketing_strategies_by_brand_marketing(
        brand_marketing_id=brand_marketing_id
    )
