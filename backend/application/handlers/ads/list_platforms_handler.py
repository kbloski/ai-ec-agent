from di.container import Container


def list_platforms_handler():
    platforms_repository = Container().platforms_repository()
    return platforms_repository.get_all()
