from typing import List


class OfferInsightDto:
    def __init__(
        self,
        id: int,
        offer_id: int,
        knowledge_id: int,
        type: str,
        status: str,
        value: str,
    ):
        self.id = id
        self.offer_id = offer_id
        self.knowledge_id = knowledge_id
        self.type = type
        self.status = status
        self.value = value