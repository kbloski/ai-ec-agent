from di.container import Container


def delete_page_content_plan_handler(id: int):
    container = Container()
    page_content_plan_repository = container.page_content_plan_repository()

    deleted = page_content_plan_repository.delete(id=id)

    return {"deleted": deleted}
