from domain.models.analysis.analysis import Analysis
from application.dtos.analysis.analysis_dto import AnalysisDto

class AnalysisMapper:

    @staticmethod
    def to_dto(item : Analysis) -> AnalysisDto:
        return AnalysisDto(
            id = item.id,
        )

