from di.container import Container


def delete_marketing_strategy_handler(id: int):
    container = Container()
    marketing_strategy_repository = container.marketing_strategy_repository()

    deleted = marketing_strategy_repository.delete(id=id)

    return {"deleted": deleted}
