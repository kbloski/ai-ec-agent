from di.container import Container


def delete_creative_execution_handler(id: int):
    container = Container()
    creative_execution_repository = container.creative_execution_repository()

    deleted = creative_execution_repository.delete(id=id)

    return {"deleted": deleted}
