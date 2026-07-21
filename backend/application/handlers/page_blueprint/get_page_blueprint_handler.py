from di.container import Container


def get_page_blueprint_handler(
    id: int,
):
    container = Container()

    page_blueprint_service = container.page_blueprint_service()

    return page_blueprint_service.get_page_blueprint_by_id(id=id)
