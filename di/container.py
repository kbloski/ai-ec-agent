from dependency_injector import containers, providers
from infrastructure.logging.logger import Logger
from infrastructure.parsers.docx_parser import DocxParser


class Container(containers.DeclarativeContainer):

    logger = providers.Singleton(
        Logger,
        name="app-logger"
    )

    docx_parser = providers.Singleton(
        DocxParser,
        logger=logger
    )