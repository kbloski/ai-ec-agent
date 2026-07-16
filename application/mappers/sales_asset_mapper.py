from domain.models.sales_assets.sales_assets import SalesAsset
from application.dtos.sales_assets.sales_asset_dto import SalesAssetDto


class SalesAssetMapper:

    @staticmethod
    def to_dto(item: SalesAsset) -> SalesAssetDto:
        return SalesAssetDto(
            id=item.id,
            knowledge_id=item.knowledge_id,
            type=item.type,
            name=item.name,
            main_angle=item.main_angle,
            content_status=item.content_status,
            version=item.version,
        )
