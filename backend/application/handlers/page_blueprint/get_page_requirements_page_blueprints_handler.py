from di.container import Container


def get_page_requirements_page_blueprints_handler(
    page_requirements_id: int,
):
    container = Container()

    page_blueprint_service = container.page_blueprint_service()

    return page_blueprint_service.get_page_blueprints_by_page_requirements(
        page_requirements_id=page_requirements_id
    )
