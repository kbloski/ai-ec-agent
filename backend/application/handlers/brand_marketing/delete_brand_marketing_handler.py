from di.container import Container


def delete_brand_marketing_handler(id: int):
    container = Container()
    brand_marketing_repository = container.brand_marketing_repository()

    deleted = brand_marketing_repository.delete(id=id)

    return {"deleted": deleted}
