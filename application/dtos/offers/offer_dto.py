from decimal import Decimal
from typing import List
from .offer_item_dto import OfferItemDto


class OfferDto:
    def __init__(
        self,
        name: str,
        buying_price: Decimal,
        selling_price: Decimal,
        details: str,
        offer_items: List[OfferItemDto],
    ):
        self.name = name
        self.buying_price = buying_price
        self.selling_price = selling_price
        self.details = details
        self.offer_items = offer_items