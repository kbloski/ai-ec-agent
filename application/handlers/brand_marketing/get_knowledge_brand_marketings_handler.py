from di.container import Container


def get_knowledge_brand_marketings_handler(
    knowledge_id: int,
):
    container = Container()

    brand_marketing_service = container.brand_marketing_service()

    return brand_marketing_service.get_brand_marketings_by_knowledge(knowledge_id=knowledge_id)
