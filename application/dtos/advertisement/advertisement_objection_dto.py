from typing import Optional

from common.mixins.json_serializable import JSONSerializable


class AdvertisementObjectionDto(JSONSerializable):
    def __init__(
        self,
        id: int,
        advertisement_id: int,
        objection: str,
        answer: Optional[str],
    ):
        self.id = id
        self.advertisement_id = advertisement_id
        self.objection = objection
        self.answer = answer

    def to_dict(self, exclude=None):
        exclude = set(exclude or [])

        data = {
            "id": self.id,
            "advertisement_id": self.advertisement_id,
            "objection": self.objection,
            "answer": self.answer,
        }

        return {k: v for k, v in data.items() if k not in exclude}
