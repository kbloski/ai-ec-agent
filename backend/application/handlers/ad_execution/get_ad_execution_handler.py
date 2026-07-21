from di.container import Container


def get_ad_execution_handler(
    id: int,
):
    container = Container()

    ad_execution_service = container.ad_execution_service()

    return ad_execution_service.get_ad_execution_by_id(id=id)
