from di.container import Container


def get_page_strategy_page_blueprints_handler(
    page_strategy_id: int,
):
    container = Container()

    page_blueprint_service = container.page_blueprint_service()

    return page_blueprint_service.get_page_blueprints_by_page_strategy(
        page_strategy_id=page_strategy_id
    )
