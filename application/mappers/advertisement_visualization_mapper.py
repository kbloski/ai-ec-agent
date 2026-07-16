from domain.models.advertisement.advertisement_visualization import AdvertisementVisualization
from application.dtos.advertisement.advertisement_visualization_dto import (
    AdvertisementVisualizationDto,
)


class AdvertisementVisualizationMapper:

    @staticmethod
    def to_dto(item: AdvertisementVisualization) -> AdvertisementVisualizationDto:
        return AdvertisementVisualizationDto(
            id=item.id,
            advertisement_id=item.advertisement_id,
            scene_id=item.scene_id,
            order_number=item.order_number,
            type=item.type,
            description=item.description,
        )
