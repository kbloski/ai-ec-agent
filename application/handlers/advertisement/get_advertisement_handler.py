from di.container import Container


# =====================================================
# MAIN HANDLER
# =====================================================

def get_advertisement_handler(
    id: int,
):
    container = Container()

    advertisement_service = container.advertisement_service()

    return advertisement_service.get_advertisement_details_by_id(id=id)
