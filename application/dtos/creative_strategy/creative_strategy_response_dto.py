from typing import Optional, List

from common.mixins.json_serializable import JSONSerializable


class CreativeStrategyDto(JSONSerializable):

    def __init__(
        self,
        id: int,
        knowledge_id: int,
        brand_marketing_id: int,
        marketing_strategy_id: int,
        offer_strategy_id: int,
        message_strategy_id: int,
        ad_strategy_id: int,
        name: Optional[str],
        execution: Optional[dict],
        script: Optional[List[dict]],
        asset_requirements: Optional[List[dict]],
        production_notes: Optional[dict],
        cta: Optional[dict],
    ):
        self.id = id
        self.knowledge_id = knowledge_id
        self.brand_marketing_id = brand_marketing_id
        self.marketing_strategy_id = marketing_strategy_id
        self.offer_strategy_id = offer_strategy_id
        self.message_strategy_id = message_strategy_id
        self.ad_strategy_id = ad_strategy_id
        self.name = name
        self.execution = execution
        self.script = script
        self.asset_requirements = asset_requirements
        self.production_notes = production_notes
        self.cta = cta

    def to_dict(self, exclude=None):
        exclude = set(exclude or [])

        data = {
            "id": self.id,
            "knowledge_id": self.knowledge_id,
            "brand_marketing_id": self.brand_marketing_id,
            "marketing_strategy_id": self.marketing_strategy_id,
            "offer_strategy_id": self.offer_strategy_id,
            "message_strategy_id": self.message_strategy_id,
            "ad_strategy_id": self.ad_strategy_id,
            "name": self.name,
            "execution": self.execution,
            "script": self.script,
            "asset_requirements": self.asset_requirements,
            "production_notes": self.production_notes,
            "cta": self.cta,
        }

        return {k: v for k, v in data.items() if k not in exclude}
