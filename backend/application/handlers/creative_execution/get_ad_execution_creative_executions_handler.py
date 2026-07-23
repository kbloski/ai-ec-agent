from di.container import Container


def get_ad_execution_creative_executions_handler(
    ad_execution_id: int,
):
    container = Container()

    creative_execution_service = container.creative_execution_service()

    return creative_execution_service.get_creative_executions_by_ad_execution(
        ad_execution_id=ad_execution_id
    )
