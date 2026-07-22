from di.container import Container


def get_video_creative_execution_handler(
    id: int,
):
    container = Container()

    video_creative_execution_service = container.video_creative_execution_service()

    return video_creative_execution_service.get_video_creative_execution_by_id(id=id)
