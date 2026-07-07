from dependency_injector import containers, providers
from application.services.knowledge_service import KnowledgeService
from application.services.ollama_service import OllamaService
from application.services.product_service import ProductService
from infrastructure.logging.logger import Logger
from infrastructure.parsers.docx_parser import DocxParser
from infrastructure.repositories.offers_repository import OffersRepository
from infrastructure.repositories.offer_items_repository import OfferItemsRepository
from infrastructure.services.path_service import PathService
from infrastructure.parsers.txt_parser import TxtParser
from core.settings import Settings
from infrastructure.database.db import SessionLocal
from application.assemblers.offer_assembler import OfferAssembler
from infrastructure.repositories.offers_knowledge_repository import OfferKnowledgeRepository
from infrastructure.repositories.offer_insights_repository import OfferInsightsRepository
from application.assemblers.offer_knowledge_assembler import OfferKnowledgeAssembler

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

    offers_repository =  providers.Singleton(
        OffersRepository,
        logger=logger,
        db=db
    )

    offer_items_repository =  providers.Singleton(
        OfferItemsRepository,
        logger=logger,
        db=db
    )

    offer_knowledge_repository = providers.Singleton(
        OfferKnowledgeRepository,
        logger=logger,
        db=db
    )

    offer_insights_repository = providers.Singleton(
        OfferInsightsRepository,
        logger=logger,
        db=db
    )

    offer_assembler = providers.Singleton(
        OfferAssembler,
        logger=logger,
        offers_repository=offers_repository,
        offer_items_repository=offer_items_repository
    )

    offer_knowledge_assembler = providers.Singleton(
        OfferKnowledgeAssembler,
        logger=logger,
        offer_knowledge_repository=offer_knowledge_repository,
        offer_insights_repository=offer_insights_repository
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
        offers_repository=offers_repository,
        ollama_service=ollama_service,
        path_service=path_service
    )
    

