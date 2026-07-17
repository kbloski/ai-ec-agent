from typing import Optional, List

from common.mixins.json_serializable import JSONSerializable
from application.dtos.experiments.experiment_response_dto import ExperimentDto


class ExperimentStrategyDto(JSONSerializable):

    def __init__(
        self,
        id: int,
        knowledge_id: int,
        brand_marketing_id: int,
        marketing_strategy_id: int,
        offer_strategy_id: int,
        message_strategy_id: int,
        experiment_strategy: Optional[str],
        learning_objectives: Optional[List[str]],
        experiments: Optional[List[ExperimentDto]] = None,
    ):
        self.id = id
        self.knowledge_id = knowledge_id
        self.brand_marketing_id = brand_marketing_id
        self.marketing_strategy_id = marketing_strategy_id
        self.offer_strategy_id = offer_strategy_id
        self.message_strategy_id = message_strategy_id
        self.experiment_strategy = experiment_strategy
        self.learning_objectives = learning_objectives
        self.experiments = experiments or []

    def to_dict(self, exclude=None):
        exclude = set(exclude or [])

        data = {
            "id": self.id,
            "knowledge_id": self.knowledge_id,
            "brand_marketing_id": self.brand_marketing_id,
            "marketing_strategy_id": self.marketing_strategy_id,
            "offer_strategy_id": self.offer_strategy_id,
            "message_strategy_id": self.message_strategy_id,
            "experiment_strategy": self.experiment_strategy,
            "learning_objectives": self.learning_objectives,
            "experiments": [item.to_dict() for item in self.experiments],
        }

        return {k: v for k, v in data.items() if k not in exclude}
