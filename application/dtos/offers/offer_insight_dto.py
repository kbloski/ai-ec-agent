from typing import List
from common.mixins.json_serializable import JSONSerializable

class OfferInsightDto(JSONSerializable):
    def __init__(
        self,
        id: int,
        offer_id: int,
        type: str,
        content_status: str,
        value: str,
    ):
        self.id = id
        self.offer_id = offer_id
        self.type = type
        self.content_status = content_status
        self.value = value

    # def to_dict(self, exclude=None):
        # return super().to_dict(exclude)