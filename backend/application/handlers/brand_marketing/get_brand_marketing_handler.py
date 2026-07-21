from di.container import Container


def get_brand_marketing_handler(
    id: int,
):
    container = Container()

    brand_marketing_service = container.brand_marketing_service()

    return brand_marketing_service.get_brand_marketing_by_id(id=id)
