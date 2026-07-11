from decimal import Decimal
from typing import List
from .offer_item_dto import OfferItemDto
from common.mixins.json_serializable import JSONSerializable

class OfferDto(JSONSerializable):
    def __init__(
        self,
        id: int,
        name: str,
        buying_price: Decimal,
        selling_price: Decimal,
        details: str,
        target_audience : List[str],
        pain_points : List[str],
        offer_items: List[OfferItemDto],
    ):
        self.id = id
        self.name = name
        self.buying_price = buying_price
        self.selling_price = selling_price
        self.details = details
        self.target_audience = target_audience
        self.pain_points = pain_points
        self.offer_items = offer_items

    def to_dict(self, exclude=None):
        self.offer_items = [i.to_dict() for i in self.offer_items]
        return super().to_dict(exclude)