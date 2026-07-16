from typing import List

from infrastructure.logging.logger import Logger
from domain.models.experiment.experiment import Experiment
from application.dtos.experiment.experiment_response_dto import ExperimentDto
from infrastructure.repositories.experiments_repository import ExperimentsRepository
from application.mappers.experiment_mapper import ExperimentMapper
from application.assemblers.experiment_assembler import ExperimentAssembler


class ExperimentService:

    def __init__(
        self,
        logger: Logger,
        experiments_repository: ExperimentsRepository,
        experiment_assembler: ExperimentAssembler,
    ):
        self.logger = logger
        self.experiments_repository = experiments_repository
        self.experiment_assembler = experiment_assembler

    def create_experiment(self, experiment: Experiment) -> ExperimentDto:
        created = self.experiments_repository.create(experiment)
        return self.get_experiment_by_id(id=created.id)

    def get_experiment_by_id(self, id: int) -> ExperimentDto:
        experiment_db = self.experiments_repository.get_by_id(id)

        if not experiment_db:
            raise ValueError(f"Experiment {id} not found")

        experiment_dto = ExperimentMapper.to_dto(experiment_db)
        return self.experiment_assembler.assemble_dto(experiment_dto)

    def get_experiments_by_knowledge(self, knowledge_id: int) -> List[ExperimentDto]:
        items = self.experiments_repository.get_by_knowledge_id(knowledge_id)
        dtos = [ExperimentMapper.to_dto(item) for item in items]
        return [self.experiment_assembler.assemble_dto(dto) for dto in dtos]
