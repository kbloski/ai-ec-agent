from dependency_injector import containers, providers
from application.services.knowledge_service import KnowledgeService
from application.services.ollama_service import OllamaService
from application.services.product_service import ProductService
from infrastructure.logging.logger import Logger
from infrastructure.parsers.docx_parser import DocxParser
from infrastructure.repositories.products_repository import ProductRepository
from infrastructure.services.path_service import PathService
from infrastructure.parsers.txt_parser import TxtParser
from core.settings import Settings
from infrastructure.database.db import SessionLocal
class Container(containers.DeclarativeContainer):
    db = providers.Factory(
        SessionLocal
    )

    logger = providers.Singleton(
        Logger,
        name="app-logger"
    )

    settings = providers.Singleton(
        Settings
    )

    docx_parser = providers.Singleton(
        DocxParser,
        logger=logger
    )

    txt_parser = providers.Singleton(
        TxtParser,
        logger=logger
    )

    path_service =  providers.Singleton(
        PathService,
        logger=logger,
    )

    product_repository =  providers.Singleton(
        ProductRepository,
        logger=logger,
        db=db
    )

    ollama_service =  providers.Singleton(
        OllamaService,
        logger=logger,
        settings=settings
    )

    knowledge_service = providers.Singleton(
        KnowledgeService,
        logger=logger,
        docx_parser=docx_parser,
        txt_parser=txt_parser,
        path_service=path_service,
        ollama_service=ollama_service
    )

    product_service = providers.Singleton(
        ProductService,
        logger=logger,
        product_repository=product_repository,
        ollama_service=ollama_service
    )
    

