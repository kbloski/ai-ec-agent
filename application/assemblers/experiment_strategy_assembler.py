from infrastructure.logging.logger import Logger
from application.dtos.experiment_strategy.experiment_strategy_response_dto import ExperimentStrategyDto
from application.mappers.experiment_item_mapper import ExperimentItemMapper
from infrastructure.repositories.experiments_repository import ExperimentsRepository


class ExperimentStrategyAssembler:
    def __init__(self, logger: Logger, experiments_repository: ExperimentsRepository):
        self.logger = logger
        self.experiments_repository = experiments_repository

    def assemble_dto(self, item: ExperimentStrategyDto) -> ExperimentStrategyDto:
        experiments_db = self.experiments_repository.get_by_experiment_strategy_id(
            experiment_strategy_id=item.id
        )
        item.experiments = [ExperimentItemMapper.to_dto(i) for i in experiments_db]

        return item
