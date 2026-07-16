from typing import Optional

from common.mixins.json_serializable import JSONSerializable


class AdvertisementVisualizationDto(JSONSerializable):
    def __init__(
        self,
        id: int,
        advertisement_id: int,
        scene_id: Optional[int],
        order_number: int,
        type: Optional[str],
        description: Optional[str],
    ):
        self.id = id
        self.advertisement_id = advertisement_id
        self.scene_id = scene_id
        self.order_number = order_number
        self.type = type
        self.description = description

    def to_dict(self, exclude=None):
        exclude = set(exclude or [])

        data = {
            "id": self.id,
            "advertisement_id": self.advertisement_id,
            "scene_id": self.scene_id,
            "order_number": self.order_number,
            "type": self.type,
            "description": self.description,
        }

        return {k: v for k, v in data.items() if k not in exclude}
