from di.container import Container


def get_page_content_plan_page_copies_handler(
    page_content_plan_id: int,
):
    container = Container()

    page_copy_service = container.page_copy_service()

    return page_copy_service.get_page_copies_by_page_content_plan(
        page_content_plan_id=page_content_plan_id
    )
