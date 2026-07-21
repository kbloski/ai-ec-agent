from typing import Optional
from common.mixins.json_serializable import JSONSerializable


class AnalysisQuestionDto(JSONSerializable):
    def __init__(
        self,
        id: int,
        analysis_id: int,
        question: str,
        answer: Optional[str],
        score: Optional[int],
        confidence: Optional[float]
    ):
        self.id = id
        self.analysis_id = analysis_id
        self.question = question
        self.answer = answer
        self.score = score
        self.confidence = confidence

    def to_dict(self, exclude=None):
        exclude = set(exclude or [])

        data = {
            "id": self.id,
            "analysis_id": self.analysis_id,
            "question": self.question,
            "answer": self.answer,
            "score": self.score,
            "confidence": self.confidence
        }

        return {
            k: v for k, v in data.items()
            if k not in exclude
        }