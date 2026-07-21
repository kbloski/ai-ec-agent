from di.container import Container


def delete_offer_handler(id: int):
    container = Container()
    offers_repository = container.offers_repository()
    offer_items_repository = container.offer_items_repository()

    offer_items = offer_items_repository.get_by_offer_id(offer_id=id)
    for offer_item in offer_items:
        offer_items_repository.delete(id=offer_item.id)

    deleted = offers_repository.delete(id=id)

    return {"deleted": deleted}
