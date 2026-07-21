from di.container import Container


def get_creative_strategy_ad_executions_handler(
    creative_strategy_id: int,
):
    container = Container()

    ad_execution_service = container.ad_execution_service()

    return ad_execution_service.get_ad_executions_by_creative_strategy(
        creative_strategy_id=creative_strategy_id
    )
