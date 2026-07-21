from di.container import Container


def delete_creative_strategy_handler(id: int):
    container = Container()
    creative_strategy_repository = container.creative_strategy_repository()

    deleted = creative_strategy_repository.delete(id=id)

    return {"deleted": deleted}
