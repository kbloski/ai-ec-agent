from di.container import Container


def get_page_requirements_handler(id: int):
    container = Container()
    page_requirements_service = container.page_requirements_service()
    return page_requirements_service.get_page_requirements_by_id(id=id)
