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
from infrastructure.repositories.knowledge_insights_repository import KnowledgeInsightsRepository
from application.assemblers.offer_knowledge_assembler import OfferKnowledgeAssembler
from infrastructure.repositories.offer_insights_repository import OfferInsightsRepository
from infrastructure.repositories.target_audiences_repository import TargetAudiencesRepository
from application.assemblers.target_audience_assembler import TargetAudienceAssembler

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

    # --------------------------
    # Parsery
    # --------------------------

    docx_parser = providers.Singleton(
        DocxParser,
        logger=logger
    )

    txt_parser = providers.Singleton(
        TxtParser,
        logger=logger
    )

    # --------------------------
    # Repozytoria
    # --------------------------

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

    knowledge_insights_repository = providers.Singleton(
        KnowledgeInsightsRepository,
        logger=logger,
        db=db
    )

    offer_insights_repository = providers.Singleton(
        OfferInsightsRepository,
        logger=logger,
        db=db
    )

    target_audiences_repository = providers.Singleton(
        TargetAudiencesRepository,
        logger=logger,
        db=db
    )

    # --------------------------
    # Assemblry
    # --------------------------

    offer_assembler = providers.Singleton(
        OfferAssembler,
        logger=logger,
        offers_repository=offers_repository,
        offer_items_repository=offer_items_repository,
        offer_insights_repository=offer_insights_repository
    )

    offer_knowledge_assembler = providers.Singleton(
        OfferKnowledgeAssembler,
        logger=logger,
        offer_knowledge_repository=offer_knowledge_repository,
        knowledge_insights_repository=knowledge_insights_repository,
        target_audiences_repository=target_audiences_repository
    )

    target_audience_assembler =  providers.Singleton(
        TargetAudienceAssembler,
        logger=logger,
    )


    # --------------------------
    # Serwisy
    # --------------------------
    
    path_service =  providers.Singleton(
        PathService,
        logger=logger,
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
    

