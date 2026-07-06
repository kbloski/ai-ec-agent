class OfferItemDto:
    def __init__(
        self,
        id: int,
        offer_id: int,
        name: str,
        quantity: int,
        details: str | None = None,
    ):
        self.id = id
        self.offer_id = offer_id
        self.name = name
        self.quantity = quantity
        self.details = details