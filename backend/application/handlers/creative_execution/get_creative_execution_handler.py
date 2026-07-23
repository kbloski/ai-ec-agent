from di.container import Container


def get_creative_execution_handler(
    id: int,
):
    container = Container()

    creative_execution_service = container.creative_execution_service()

    return creative_execution_service.get_creative_execution_by_id(id=id)
