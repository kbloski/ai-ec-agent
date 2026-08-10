from di.container import Container


def list_execution_styles_handler():
    execution_styles_repository = Container().execution_styles_repository()
    return execution_styles_repository.get_all()
