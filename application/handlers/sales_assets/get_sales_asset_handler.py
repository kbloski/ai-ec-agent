from di.container import Container


# =====================================================
# MAIN HANDLER
# =====================================================

def get_sales_asset_handler(
    id: int,
):
    container = Container()

    sales_asset_service = container.sales_asset_service()

    return sales_asset_service.get_sales_assets_details_by_id(id=id)
