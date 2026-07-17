from domain.models.experiments.experiment import Experiment
from application.dtos.experiments.experiment_response_dto import ExperimentDto


class ExperimentItemMapper:

    @staticmethod
    def to_dto(item: Experiment) -> ExperimentDto:
        return ExperimentDto(
            id=item.id,
            experiment_strategy_id=item.experiment_strategy_id,
            name=item.name,
            category=item.category,
            strategic_question=item.strategic_question,
            objective=item.objective,
            hypothesis=item.hypothesis,
            hypothesis_basis=item.hypothesis_basis,
            reason=item.reason,
            target_audience=item.target_audience,
            funnel_stage=item.funnel_stage,
            channel=item.channel,
            asset_type=item.asset_type,
            variable_tested=item.variable_tested,
            control_variant=item.control_variant,
            test_variant=item.test_variant,
            success_metrics=item.success_metrics,
            decision_rule=item.decision_rule,
            expected_learning=item.expected_learning,
            priority=item.priority,
            estimated_cost=item.estimated_cost,
            estimated_duration=item.estimated_duration,
            status=item.status,
        )
