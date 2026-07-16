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
from infrastructure.repositories.analysis_repository import AnalysisRepository
from infrastructure.repositories.knowledge_analysis_repository import KnowledgeAnalysisRepository
from application.assemblers.analysis_assembler import AnalysisAssembler
from infrastructure.repositories.analysis_questions_repository import AnalysisQuestionsRepository
from infrastructure.repositories.checklist_repository import ChecklistRepository
from infrastructure.repositories.checklist_items_repository import ChecklistItemsRepository
from infrastructure.repositories.analysis_checklist_repository import AnalysisChecklistRepository
from application.assemblers.checklist_assembler import ChecklistAssembler
from infrastructure.repositories.sales_assets_repository import SalesAssetsRepository
from infrastructure.repositories.sales_asset_sections_repository import SalesAssetSectionsRepository
from infrastructure.repositories.sales_asset_section_visualizations_repository import SalesAssetSectionVisualizationsRepository
from infrastructure.repositories.visualizations_repository import VisualizationsRepository
from application.assemblers.sales_asset_assembler import SalesAssetAssembler
from application.services.sales_asset_service import SalesAssetService

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

    checklist_repository = providers.Singleton(
        ChecklistRepository,
        logger=logger,
        db=db
    )

    checklist_items_repository = providers.Singleton(
        ChecklistItemsRepository,
        logger=logger,
        db=db
    )

    analysis_repository = providers.Singleton(
        AnalysisRepository,
        logger=logger,
        db=db
    )

    analysis_questions_repository = providers.Singleton(
        AnalysisQuestionsRepository,
        logger=logger,
        db=db
    )

    knowledge_analysis_repository = providers.Singleton(
        KnowledgeAnalysisRepository,
        logger=logger,
        db=db
    )

    analysis_checklist_repository = providers.Singleton(
        AnalysisChecklistRepository,
        logger=logger,
        db=db
    )

    sales_assets_repository = providers.Singleton(
        SalesAssetsRepository,
        logger=logger,
        db=db
    )

    sales_asset_sections_repository = providers.Singleton(
        SalesAssetSectionsRepository,
        logger=logger,
        db=db
    )

    sales_asset_section_visualizations_repository = providers.Singleton(
        SalesAssetSectionVisualizationsRepository,
        logger=logger,
        db=db
    )

    visualizations_repository = providers.Singleton(
        VisualizationsRepository,
        logger=logger,
        db=db
    )


    # --------------------------
    # Assemblery
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

    analysis_assembler = providers.Singleton(
        AnalysisAssembler,
        logger=logger,
        analysis_questions_repository=analysis_questions_repository
    )

    checklist_assembler = providers.Singleton(
        ChecklistAssembler,
        logger=logger,
        checklist_items_repository=checklist_items_repository
    )

    sales_asset_assembler = providers.Singleton(
        SalesAssetAssembler,
        logger=logger,
        sales_asset_sections_repository=sales_asset_sections_repository,
        sales_asset_section_visualizations_repository=sales_asset_section_visualizations_repository,
        visualizations_repository=visualizations_repository
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
        ollama_service=ollama_service,
        offer_knowledge_repository=offer_knowledge_repository,
        offer_knowledge_assembler=offer_knowledge_assembler
    )

    product_service = providers.Singleton(
        ProductService,
        logger=logger,
        offers_repository=offers_repository,
        ollama_service=ollama_service,
        path_service=path_service
    )

    sales_asset_service = providers.Singleton(
        SalesAssetService,
        logger=logger,
        sales_assets_repository=sales_assets_repository,
        sales_asset_assembler=sales_asset_assembler
    )
    

