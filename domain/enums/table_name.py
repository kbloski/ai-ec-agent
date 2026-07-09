from enum import Enum


class TableName(str, Enum):
    OFFERS = "offers"
    OFFER_ITEMS = "offer_items"
    OFFER_KNOWLEDGE = "offer_knowledge"
    OFFER_INSIGHTS = "offer_insights"
    TARGET_AUDIENCES = "target_audiences"