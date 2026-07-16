from infrastructure.logging.logger import Logger
from application.dtos.sales_assets.sales_asset_dto import SalesAssetDto
from infrastructure.repositories.sales_assets_repository import SalesAssetsRepository
from application.mappers.sales_asset_mapper import SalesAssetMapper
from application.assemblers.sales_asset_assembler import SalesAssetAssembler


class SalesAssetService:

    def __init__(
        self,
        logger: Logger,
        sales_assets_repository: SalesAssetsRepository,
        sales_asset_assembler: SalesAssetAssembler,
    ):
        self.logger = logger
        self.sales_assets_repository = sales_assets_repository
        self.sales_asset_assembler = sales_asset_assembler

    def get_sales_assets_details_by_id(self, id: int) -> SalesAssetDto:
        sales_asset_db = self.sales_assets_repository.get_by_id(id)

        if not sales_asset_db:
            raise ValueError(f"Sales asset {id} not found")

        sales_asset_dto = SalesAssetMapper.to_dto(sales_asset_db)
        assembled_sales_asset = self.sales_asset_assembler.assemble_dto(sales_asset_dto)
        return assembled_sales_asset
