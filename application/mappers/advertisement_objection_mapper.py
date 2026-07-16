from domain.models.advertisement.advertisement_objection import AdvertisementObjection
from application.dtos.advertisement.advertisement_objection_dto import AdvertisementObjectionDto


class AdvertisementObjectionMapper:

    @staticmethod
    def to_dto(item: AdvertisementObjection) -> AdvertisementObjectionDto:
        return AdvertisementObjectionDto(
            id=item.id,
            advertisement_id=item.advertisement_id,
            objection=item.objection,
            answer=item.answer,
        )
