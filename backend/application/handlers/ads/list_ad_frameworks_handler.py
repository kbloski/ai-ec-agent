from di.container import Container


def list_ad_frameworks_handler():
    container = Container()
    ad_frameworks_repository = container.ad_frameworks_repository()
    return ad_frameworks_repository.get_all()
