from di.container import Container


def delete_ad_execution_handler(id: int):
    container = Container()
    ad_execution_repository = container.ad_execution_repository()

    deleted = ad_execution_repository.delete(id=id)

    return {"deleted": deleted}
