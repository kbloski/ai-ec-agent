from di.container import Container


def get_page_blueprint_page_content_plans_handler(
    page_blueprint_id: int,
):
    container = Container()

    page_content_plan_service = container.page_content_plan_service()

    return page_content_plan_service.get_page_content_plans_by_page_blueprint(
        page_blueprint_id=page_blueprint_id
    )
