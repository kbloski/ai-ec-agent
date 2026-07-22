from di.container import Container


def delete_video_creative_execution_handler(id: int):
    container = Container()
    video_creative_execution_repository = container.video_creative_execution_repository()

    deleted = video_creative_execution_repository.delete(id=id)

    return {"deleted": deleted}
