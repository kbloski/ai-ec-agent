from infrastructure.logging.logger import Logger
from application.dtos.sales_assets.sales_asset_dto import SalesAssetDto
from application.mappers.sales_asset_section_mapper import SalesAssetSectionMapper
from application.mappers.sales_asset_section_visualization_mapper import (
    SalesAssetSectionVisualizationMapper,
)
from application.mappers.visualization_mapper import VisualizationMapper
from infrastructure.repositories.sales_asset_sections_repository import (
    SalesAssetSectionsRepository,
)
from infrastructure.repositories.sales_asset_section_visualizations_repository import (
    SalesAssetSectionVisualizationsRepository,
)
from infrastructure.repositories.visualizations_repository import VisualizationsRepository


class SalesAssetAssembler:
    logger: Logger
    sales_asset_sections_repository: SalesAssetSectionsRepository
    sales_asset_section_visualizations_repository: SalesAssetSectionVisualizationsRepository
    visualizations_repository: VisualizationsRepository

    def __init__(
        self,
        logger: Logger,
        sales_asset_sections_repository: SalesAssetSectionsRepository,
        sales_asset_section_visualizations_repository: SalesAssetSectionVisualizationsRepository,
        visualizations_repository: VisualizationsRepository,
    ):
        self.logger = logger
        self.sales_asset_sections_repository = sales_asset_sections_repository
        self.sales_asset_section_visualizations_repository = (
            sales_asset_section_visualizations_repository
        )
        self.visualizations_repository = visualizations_repository

    def assemble_dto(self, item: SalesAssetDto) -> SalesAssetDto:
        sections_db = self.sales_asset_sections_repository.find_for_sales_asset(
            sales_asset_id=item.id
        )
        sections_dtos = [SalesAssetSectionMapper.to_dto(i) for i in sections_db]

        for section_dto in sections_dtos:
            joins_db = self.sales_asset_section_visualizations_repository.find_by_section_id(
                sales_asset_section_id=section_dto.id
            )
            join_dtos = [SalesAssetSectionVisualizationMapper.to_dto(i) for i in joins_db]

            for join_dto in join_dtos:
                visualization_db = self.visualizations_repository.get_by_id(
                    id=join_dto.visualization_id
                )
                if visualization_db is not None:
                    join_dto.visualization = VisualizationMapper.to_dto(visualization_db)

            section_dto.visualizations = join_dtos

        item.sections = sections_dtos

        return item
