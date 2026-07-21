from di.container import Container


def delete_offer_insight_handler(id: int):
    container = Container()
    offer_insights_repository = container.offer_insights_repository()

    deleted = offer_insights_repository.delete(id=id)

    return {"deleted": deleted}
