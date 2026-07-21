from di.container import Container


def delete_ugc_creative_handler(id: int):
    container = Container()
    ugc_creative_repository = container.ugc_creative_repository()

    deleted = ugc_creative_repository.delete(id=id)

    return {"deleted": deleted}
