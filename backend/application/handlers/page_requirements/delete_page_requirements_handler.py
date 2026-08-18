from di.container import Container


def delete_page_requirements_handler(id: int):
    container = Container()
    page_requirements_repository = container.page_requirements_repository()

    deleted = page_requirements_repository.delete(id=id)

    return {"deleted": deleted}
