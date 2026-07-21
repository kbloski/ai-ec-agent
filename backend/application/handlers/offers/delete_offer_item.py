from di.container import Container


def delete_offer_item_handler(id: int):
    container = Container()
    offer_items_repository = container.offer_items_repository()

    deleted = offer_items_repository.delete(id=id)

    return {"deleted": deleted}
