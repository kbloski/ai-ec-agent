from infrastructure.logging.logger import Logger
from application.dtos.advertisement.advertisement_dto import AdvertisementDto
from infrastructure.repositories.advertisements_repository import AdvertisementsRepository
from application.mappers.advertisement_mapper import AdvertisementMapper
from application.assemblers.advertisement_assembler import AdvertisementAssembler


class AdvertisementService:

    def __init__(
        self,
        logger: Logger,
        advertisements_repository: AdvertisementsRepository,
        advertisement_assembler: AdvertisementAssembler,
    ):
        self.logger = logger
        self.advertisements_repository = advertisements_repository
        self.advertisement_assembler = advertisement_assembler

    def get_advertisement_details_by_id(self, id: int) -> AdvertisementDto:
        advertisement_db = self.advertisements_repository.get_by_id(id)

        if not advertisement_db:
            raise ValueError(f"Advertisement {id} not found")

        advertisement_dto = AdvertisementMapper.to_dto(advertisement_db)
        assembled_advertisement = self.advertisement_assembler.assemble_dto(advertisement_dto)
        return assembled_advertisement
