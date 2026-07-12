from decimal import Decimal
from typing import List

from .offer_item_dto import OfferItemDto
from .offer_insight_dto import OfferInsightDto
from common.mixins.json_serializable import JSONSerializable


class OfferDto(JSONSerializable):
    offer_items: List[OfferItemDto] = []
    offer_insights: List[OfferInsightDto] = []

    def __init__(
        self,
        id: int,
        name: str,
        buying_price: Decimal,
        selling_price: Decimal | None,
        details: str,
    ):
        self.id = id
        self.name = name
        self.buying_price = buying_price
        self.selling_price = selling_price
        self.details = details

    def to_dict(self, exclude=None):
        exclude = set(exclude or [])

        data = {
            "id": self.id,
            "name": self.name,
            "buying_price": float(self.buying_price),
            "selling_price": float(self.selling_price) if self.selling_price is not None else None,
            "details": self.details,
            "offer_items": [item.to_dict() for item in self.offer_items],
            "offer_insights": [item.to_dict() for item in self.offer_insights],
        }

        return {k: v for k, v in data.items() if k not in exclude}