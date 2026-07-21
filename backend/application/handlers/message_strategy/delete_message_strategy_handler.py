from di.container import Container


def delete_message_strategy_handler(id: int):
    container = Container()
    message_strategy_repository = container.message_strategy_repository()

    deleted = message_strategy_repository.delete(id=id)

    return {"deleted": deleted}
