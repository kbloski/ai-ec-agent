from di.container import Container


def get_page_copy_handler(
    id: int,
):
    container = Container()

    page_copy_service = container.page_copy_service()

    return page_copy_service.get_page_copy_by_id(id=id)
