from di.container import Container


def get_message_strategy_ugc_creatives_handler(
    message_strategy_id: int,
):
    container = Container()

    ugc_creative_service = container.ugc_creative_service()

    return ugc_creative_service.get_ugc_creatives_by_message_strategy(
        message_strategy_id=message_strategy_id
    )
