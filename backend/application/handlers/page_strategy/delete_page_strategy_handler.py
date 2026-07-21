from di.container import Container


def delete_page_strategy_handler(id: int):
    container = Container()
    page_strategy_repository = container.page_strategy_repository()

    deleted = page_strategy_repository.delete(id=id)

    return {"deleted": deleted}
