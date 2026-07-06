from enum import Enum


class TableName(str, Enum):
    OFFERS = "offers"
    OFFER_ITEMS = "offer_items"
    OFFER_UNDERSTANDINGS = "offer_understandings"