from typing import Optional, List
from common.mixins.json_serializable import JSONSerializable
from .analysis_question_dto import AnalysisQuestionDto

class AnalysisDto(JSONSerializable):
    analysis_questions : List[AnalysisQuestionDto] = []

    def __init__(
        self,
        id: int,
    ):
        self.id = id

    def to_dict(self, exclude=None):
        exclude = set(exclude or [])

        data = {
            "id": self.id,
            "analysis_questions": [q.to_dict() for q in self.analysis_questions],
        }

        return {k: v for k, v in data.items() if k not in exclude}