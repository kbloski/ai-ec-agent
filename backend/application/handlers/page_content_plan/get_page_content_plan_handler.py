from di.container import Container


def get_page_content_plan_handler(
    id: int,
):
    container = Container()

    page_content_plan_service = container.page_content_plan_service()

    return page_content_plan_service.get_page_content_plan_by_id(id=id)
