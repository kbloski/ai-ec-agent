from infrastructure.logging.logger import Logger
from application.dtos.experiment.experiment_response_dto import ExperimentDto


class ExperimentAssembler:
    def __init__(self, logger: Logger):
        self.logger = logger

    def assemble_dto(self, item: ExperimentDto) -> ExperimentDto:
        return item
