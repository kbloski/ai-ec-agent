from di.container import Container


def list_creative_angels_handler():
    container = Container()
    creative_angels_repository = container.creative_angels_repository()
    return creative_angels_repository.get_all()
