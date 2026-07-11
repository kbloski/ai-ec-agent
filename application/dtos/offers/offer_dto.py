from decimal import Decimal
from typing import List
from .offer_item_dto import OfferItemDto
from .offer_insight_dto import OfferInsightDto
from common.mixins.json_serializable import JSONSerializable

class OfferDto(JSONSerializable):
    offer_items : List[OfferItemDto] = []
    offer_insights : List[OfferInsightDto] = []

    def __init__(
        self,
        id: int,
        name: str,
        buying_price: Decimal,
        selling_price: Decimal,
        details: str,
    ):
        self.id = id
        self.name = name
        self.buying_price = buying_price
        self.selling_price = selling_price
        self.details = details

    def to_dict(self, exclude=None):
        obj_dict = super().to_dict(exclude)
        obj_dict["offer_items"] = [i.to_dict() for i in self.offer_items]
        obj_dict["self.offer_insights"] = [i.to_dict() for i in self.offer_insights]
        return obj_dict