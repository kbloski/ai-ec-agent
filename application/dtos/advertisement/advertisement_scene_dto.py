from typing import Optional

from common.mixins.json_serializable import JSONSerializable
from application.dtos.advertisement.scene_dto import SceneDto


class AdvertisementSceneDto(JSONSerializable):
    scene: Optional[SceneDto] = None

    def __init__(
        self,
        id: int,
        advertisement_id: int,
        scene_id: int,
        order_number: int,
    ):
        self.id = id
        self.advertisement_id = advertisement_id
        self.scene_id = scene_id
        self.order_number = order_number

    def to_dict(self, exclude=None):
        exclude = set(exclude or [])

        data = {
            "id": self.id,
            "advertisement_id": self.advertisement_id,
            "scene_id": self.scene_id,
            "order_number": self.order_number,
            "scene": self.scene.to_dict() if self.scene else None,
        }

        return {k: v for k, v in data.items() if k not in exclude}
