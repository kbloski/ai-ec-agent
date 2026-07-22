from di.container import Container


def get_ad_execution_video_creative_executions_handler(
    ad_execution_id: int,
):
    container = Container()

    video_creative_execution_service = container.video_creative_execution_service()

    return video_creative_execution_service.get_video_creative_executions_by_ad_execution(
        ad_execution_id=ad_execution_id
    )
