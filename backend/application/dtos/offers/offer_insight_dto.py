from common.mixins.json_serializable import JSONSerializable

class OfferInsightDto(JSONSerializable):
    def __init__(
        self,
        id: int,
        offer_id: int,
        type: str,
        fact_status: str,
        review_status: str,
        value: str,
    ):
        self.id = id
        self.offer_id = offer_id
        self.type = type
        self.fact_status = fact_status
        self.review_status = review_status
        self.value = value

    def to_dict(self, exclude=None):
        exclude = set(exclude or [])

        data = {
            "id": self.id,
            "offer_id": self.offer_id,
            "type": self.type,
            "fact_status": self.fact_status,
            "review_status": self.review_status,
            "value": self.value,
        }

        return {k: v for k, v in data.items() if k not in exclude}
