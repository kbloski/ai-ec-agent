from di.container import Container


def list_page_sections_handler():
    container = Container()
    page_sections_service = container.page_sections_service()
    return page_sections_service.get_all()
