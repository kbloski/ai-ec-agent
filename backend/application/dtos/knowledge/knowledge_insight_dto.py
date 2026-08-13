from typing import List
from common.mixins.json_serializable import JSONSerializable

class KnowledgeInsightDto:
    def __init__(
        self,
        id: int,
        knowledge_id: int,
        type: str,
        content_status: str,
        value: str,
    ):
        self.id = id
        self.knowledge_id = knowledge_id
        self.type = type
        self.content_status = content_status
        self.value = value

    def to_dict(self, exclude=None):
        exclude = set(exclude or [])

        data = {
            "id": self.id,
            "knowledge_id" : self.knowledge_id,
            "type": self.type,
            "content_status": self.content_status,
            "value": self.value,
        }

        return {k: v for k, v in data.items() if k not in exclude}
    
    def to_content_dict(self):
        data = self.to_dict(exclude=["id", "knowledge_id"])
        return data