from domain.models.analysis.analysis_questions import AnalysisQuestion
from application.dtos.analysis.analysis_question_dto import AnalysisQuestionDto


class AnalysisQuestionMapper:

    @staticmethod
    def to_dto(item: AnalysisQuestion) -> AnalysisQuestionDto:
        return AnalysisQuestionDto(
            id=item.id,
            analysis_id=item.analysis_id,
            question=item.question,
            answer=item.answer,
            score=item.score,
            confidence=item.confidence
        )
