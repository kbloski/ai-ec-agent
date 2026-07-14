from typing import Optional, List
from common.mixins.json_serializable import JSONSerializable
from .checklist_item_dto import ChecklistItemDto

class ChecklistDto(JSONSerializable):
    checklist_items : List[ChecklistItemDto] = []

    def __init__(
        self,
        id: int,
        name: str
    ):
        self.id = id
        self.name = name

    def to_dict(self, exclude=None):
        exclude = set(exclude or [])

        data = {
            "id": self.id,
            "name" : self.name,
            "checklist_items" : self.checklist_items
        }

        return {k: v for k, v in data.items() if k not in exclude}