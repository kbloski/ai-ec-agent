from typing import Optional, List

from common.mixins.json_serializable import JSONSerializable


class PageBlueprintDto(JSONSerializable):

    def __init__(
        self,
        id: int,
        knowledge_id: int,
        brand_marketing_id: int,
        marketing_strategy_id: int,
        offer_strategy_id: int,
        message_strategy_id: int,
        page_strategy_id: int,
        page_type: Optional[str],
        primary_conversion_goal: Optional[str],
        sections: Optional[List[dict]],
    ):
        self.id = id
        self.knowledge_id = knowledge_id
        self.brand_marketing_id = brand_marketing_id
        self.marketing_strategy_id = marketing_strategy_id
        self.offer_strategy_id = offer_strategy_id
        self.message_strategy_id = message_strategy_id
        self.page_strategy_id = page_strategy_id
        self.page_type = page_type
        self.primary_conversion_goal = primary_conversion_goal
        self.sections = sections

    def to_dict(self, exclude=None):
        exclude = set(exclude or [])

        data = {
            "id": self.id,
            "knowledge_id": self.knowledge_id,
            "brand_marketing_id": self.brand_marketing_id,
            "marketing_strategy_id": self.marketing_strategy_id,
            "offer_strategy_id": self.offer_strategy_id,
            "message_strategy_id": self.message_strategy_id,
            "page_strategy_id": self.page_strategy_id,
            "page_type": self.page_type,
            "primary_conversion_goal": self.primary_conversion_goal,
            "sections": self.sections,
        }

        return {k: v for k, v in data.items() if k not in exclude}
