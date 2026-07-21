from di.container import Container


def delete_ad_strategy_handler(id: int):
    container = Container()
    ad_strategy_repository = container.ad_strategy_repository()

    deleted = ad_strategy_repository.delete(id=id)

    return {"deleted": deleted}
