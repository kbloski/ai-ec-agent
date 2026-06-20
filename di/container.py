from dependency_injector import containers, providers
from infrastructure.logging.logger import Logger
from infrastructure.parsers.docx_parser import DocxParser
from application.services.knowledge_service import KnowledgeService

class Container(containers.DeclarativeContainer):

    logger = providers.Singleton(
        Logger,
        name="app-logger"
    )

    docx_parser = providers.Singleton(
        DocxParser,
        logger=logger
    )

    knowledge_service =  providers.Singleton(
        KnowledgeService,
        logger=logger,
        docx_parser=docx_parser
    )

