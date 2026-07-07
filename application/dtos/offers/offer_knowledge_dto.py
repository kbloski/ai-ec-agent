from typing import Optional, List
from .offer_insight_dto import OfferInsightDto


class OfferKnowledgeDto:

    offer_insights: List[OfferInsightDto] = []

    def __init__(
        self,
        id: int,
        offer_id: int,
        version: int,
        status: str,
        offer_summary: Optional[str] = None,
        category: Optional[str] = None,
        value_proposition: Optional[str] = None,
    ):
        self.id = id
        self.offer_id = offer_id
        self.version = version
        self.status = status
        self.offer_summary = offer_summary
        self.category = category
        self.value_proposition = value_proposition