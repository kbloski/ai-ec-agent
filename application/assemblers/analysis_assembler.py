from infrastructure.logging.logger import Logger
from application.dtos.analysis.analysis_dto import AnalysisDto

class AnalysisAssembler:
    def __init__(
        self,
        logger : Logger,
    ):
        None

    def assemble_dto(self, item : AnalysisDto) -> AnalysisDto:
        return item
    

