from di.container import Container


def delete_offer_strategy_handler(id: int):
    container = Container()
    offer_strategy_repository = container.offer_strategy_repository()

    deleted = offer_strategy_repository.delete(id=id)

    return {"deleted": deleted}
