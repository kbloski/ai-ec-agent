from di.container import Container


def get_page_strategy_page_requirements_handler(page_strategy_id: int):
    container = Container()
    page_requirements_service = container.page_requirements_service()
    return page_requirements_service.get_page_requirements_by_page_strategy(
        page_strategy_id=page_strategy_id
    )
