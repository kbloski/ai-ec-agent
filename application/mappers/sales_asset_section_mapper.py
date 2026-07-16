from domain.models.sales_assets.sales_asset_sections import SalesAssetSection
from application.dtos.sales_assets.sales_asset_section_dto import SalesAssetSectionDto


class SalesAssetSectionMapper:

    @staticmethod
    def to_dto(item: SalesAssetSection) -> SalesAssetSectionDto:
        return SalesAssetSectionDto(
            id=item.id,
            sales_asset_id=item.sales_asset_id,
            type=item.type,
            position=item.position,
            name=item.name,
            goal=item.goal,
            headline=item.headline,
            subheadline=item.subheadline,
            content=item.content,
        )
