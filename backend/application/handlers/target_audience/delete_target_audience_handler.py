from di.container import Container


def delete_target_audience_handler(id: int):
    container = Container()
    target_audiences_repository = container.target_audiences_repository()

    deleted = target_audiences_repository.delete(id=id)

    return {"deleted": deleted}
