from di.container import Container


def delete_page_blueprint_handler(id: int):
    container = Container()
    page_blueprint_repository = container.page_blueprint_repository()

    deleted = page_blueprint_repository.delete(id=id)

    return {"deleted": deleted}
