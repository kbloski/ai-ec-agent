from di.container import Container


def get_page_strategy_handler(
    id: int,
):
    container = Container()

    page_strategy_service = container.page_strategy_service()

    return page_strategy_service.get_page_strategy_by_id(id=id)
