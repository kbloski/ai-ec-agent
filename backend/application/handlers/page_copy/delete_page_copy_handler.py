from di.container import Container


def delete_page_copy_handler(id: int):
    container = Container()
    page_copy_repository = container.page_copy_repository()

    deleted = page_copy_repository.delete(id=id)

    return {"deleted": deleted}
