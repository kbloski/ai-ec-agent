from di.container import Container


def get_message_strategy_handler(
    id: int,
):
    container = Container()

    message_strategy_service = container.message_strategy_service()

    return message_strategy_service.get_message_strategy_by_id(id=id)
