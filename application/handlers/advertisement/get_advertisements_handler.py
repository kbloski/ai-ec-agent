from di.container import Container
from application.mappers.advertisement_mapper import AdvertisementMapper


# =====================================================
# MAIN HANDLER
# =====================================================

def get_advertisements_handler(
    knowledge_id: int,
):
    container = Container()

    advertisements_repository = container.advertisements_repository()
    advertisement_assembler = container.advertisement_assembler()

    items = advertisements_repository.get_by_knowledge_id(knowledge_id)

    dtos = [AdvertisementMapper.to_dto(item) for item in items]

    return [advertisement_assembler.assemble_dto(dto) for dto in dtos]
