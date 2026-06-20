from dependency_injector import containers, providers
from infrastructure.logging.logger import Logger

class Container(containers.DeclarativeContainer):
    None
    # singleton (jedna instancja repo)
    logger = providers.Singleton(Logger, name="app-logger")


