from infrastructure.logging.logger import Logger
from domain.models.experiment_strategy.experiment_strategy import ExperimentStrategy
from application.dtos.experiment_strategy.experiment_strategy_response_dto import ExperimentStrategyDto
from infrastructure.repositories.experiment_strategy_repository import ExperimentStrategyRepository
from application.mappers.experiment_strategy_mapper import ExperimentStrategyMapper
from application.assemblers.experiment_strategy_assembler import ExperimentStrategyAssembler


class ExperimentStrategyService:

    def __init__(
        self,
        logger: Logger,
        experiment_strategy_repository: ExperimentStrategyRepository,
        experiment_strategy_assembler: ExperimentStrategyAssembler,
    ):
        self.logger = logger
        self.experiment_strategy_repository = experiment_strategy_repository
        self.experiment_strategy_assembler = experiment_strategy_assembler

    def create_experiment_strategy(self, experiment_strategy: ExperimentStrategy) -> ExperimentStrategyDto:
        created = self.experiment_strategy_repository.create(experiment_strategy)
        return self.get_experiment_strategy_by_id(id=created.id)

    def get_experiment_strategy_by_id(self, id: int) -> ExperimentStrategyDto:
        experiment_strategy_db = self.experiment_strategy_repository.get_by_id(id)

        if not experiment_strategy_db:
            raise ValueError(f"Experiment strategy {id} not found")

        experiment_strategy_dto = ExperimentStrategyMapper.to_dto(experiment_strategy_db)
        return self.experiment_strategy_assembler.assemble_dto(experiment_strategy_dto)
