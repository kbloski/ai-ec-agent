from typing import Optional

from common.mixins.json_serializable import JSONSerializable


class ChecklistItemDto(JSONSerializable):
    def __init__(
        self,
        id: int,
        checklist_id: int,
        question: str,
        answer: Optional[str],
        notes: Optional[str]
    ):
        self.id = id
        self.checklist_id = checklist_id
        self.question = question
        self.answer = answer
        self.notes = notes

    def to_dict(self, exclude=None):
        exclude = set(exclude or [])

        data = {
            "id": self.id,
            "checklist_id": self.checklist_id,
            "question": self.question,
            "answer": self.answer,
            "notes": self.notes,
        }

        return {k: v for k, v in data.items() if k not in exclude}