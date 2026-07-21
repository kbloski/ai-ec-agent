from di.container import Container


def get_ugc_creative_handler(
    id: int,
):
    container = Container()

    ugc_creative_service = container.ugc_creative_service()

    return ugc_creative_service.get_ugc_creative_by_id(id=id)
