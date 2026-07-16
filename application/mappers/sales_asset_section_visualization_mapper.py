from domain.models.sales_assets.sales_asset_section_visualization import (
    SalesAssetSectionVisualization,
)
from application.dtos.sales_assets.sales_asset_section_visualization_dto import (
    SalesAssetSectionVisualizationDto,
)


class SalesAssetSectionVisualizationMapper:

    @staticmethod
    def to_dto(item: SalesAssetSectionVisualization) -> SalesAssetSectionVisualizationDto:
        return SalesAssetSectionVisualizationDto(
            sales_asset_section_id=item.sales_asset_section_id,
            visualization_id=item.visualization_id,
            position=item.position,
        )
