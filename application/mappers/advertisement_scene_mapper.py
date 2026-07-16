from domain.models.advertisement.advertisement_scene import AdvertisementScene
from application.dtos.advertisement.advertisement_scene_dto import AdvertisementSceneDto


class AdvertisementSceneMapper:

    @staticmethod
    def to_dto(item: AdvertisementScene) -> AdvertisementSceneDto:
        return AdvertisementSceneDto(
            id=item.id,
            advertisement_id=item.advertisement_id,
            scene_id=item.scene_id,
            order_number=item.order_number,
        )
