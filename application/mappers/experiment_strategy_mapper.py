from domain.models.experiment_strategy.experiment_strategy import ExperimentStrategy
from application.dtos.experiment_strategy.experiment_strategy_response_dto import ExperimentStrategyDto


class ExperimentStrategyMapper:

    @staticmethod
    def to_dto(item: ExperimentStrategy) -> ExperimentStrategyDto:
        return ExperimentStrategyDto(
            id=item.id,
            knowledge_id=item.knowledge_id,
            brand_marketing_id=item.brand_marketing_id,
            marketing_strategy_id=item.marketing_strategy_id,
            offer_strategy_id=item.offer_strategy_id,
            message_strategy_id=item.message_strategy_id,
            experiment_strategy=item.experiment_strategy,
            learning_objectives=item.learning_objectives,
        )
