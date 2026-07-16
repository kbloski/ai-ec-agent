from di.container import Container
from application.mappers.sales_asset_mapper import SalesAssetMapper


# =====================================================
# MAIN HANDLER
# =====================================================

def get_sales_assets_handler(
    knowledge_id: int,
):
    container = Container()

    sales_assets_repository = container.sales_assets_repository()
    sales_asset_assembler = container.sales_asset_assembler()

    items = sales_assets_repository.get_by_knowledge_id(knowledge_id)

    dtos = [SalesAssetMapper.to_dto(item) for item in items]

    return [sales_asset_assembler.assemble_dto(dto) for dto in dtos]
