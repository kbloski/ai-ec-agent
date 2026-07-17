from typing import Optional, List, Dict, Any

from common.mixins.json_serializable import JSONSerializable


class ExperimentDto(JSONSerializable):

    def __init__(
        self,
        id: int,
        experiment_strategy_id: int,
        name: Optional[str],
        category: Optional[str],
        strategic_question: Optional[str],
        objective: Optional[str],
        hypothesis: Optional[str],
        hypothesis_basis: Optional[List[str]],
        reason: Optional[str],
        target_audience: Optional[str],
        funnel_stage: Optional[str],
        channel: Optional[str],
        asset_type: Optional[str],
        variable_tested: Optional[str],
        control_variant: Optional[str],
        test_variant: Optional[str],
        success_metrics: Optional[List[str]],
        decision_rule: Optional[str],
        expected_learning: Optional[str],
        priority: Optional[Dict[str, Any]],
        estimated_cost: Optional[str],
        estimated_duration: Optional[str],
        status: Optional[str],
    ):
        self.id = id
        self.experiment_strategy_id = experiment_strategy_id
        self.name = name
        self.category = category
        self.strategic_question = strategic_question
        self.objective = objective
        self.hypothesis = hypothesis
        self.hypothesis_basis = hypothesis_basis
        self.reason = reason
        self.target_audience = target_audience
        self.funnel_stage = funnel_stage
        self.channel = channel
        self.asset_type = asset_type
        self.variable_tested = variable_tested
        self.control_variant = control_variant
        self.test_variant = test_variant
        self.success_metrics = success_metrics
        self.decision_rule = decision_rule
        self.expected_learning = expected_learning
        self.priority = priority
        self.estimated_cost = estimated_cost
        self.estimated_duration = estimated_duration
        self.status = status

    def to_dict(self, exclude=None):
        exclude = set(exclude or [])

        data = {
            "id": self.id,
            "experiment_strategy_id": self.experiment_strategy_id,
            "name": self.name,
            "category": self.category,
            "strategic_question": self.strategic_question,
            "objective": self.objective,
            "hypothesis": self.hypothesis,
            "hypothesis_basis": self.hypothesis_basis,
            "reason": self.reason,
            "target_audience": self.target_audience,
            "funnel_stage": self.funnel_stage,
            "channel": self.channel,
            "asset_type": self.asset_type,
            "variable_tested": self.variable_tested,
            "control_variant": self.control_variant,
            "test_variant": self.test_variant,
            "success_metrics": self.success_metrics,
            "decision_rule": self.decision_rule,
            "expected_learning": self.expected_learning,
            "priority": self.priority,
            "estimated_cost": self.estimated_cost,
            "estimated_duration": self.estimated_duration,
            "status": self.status,
        }

        return {k: v for k, v in data.items() if k not in exclude}
