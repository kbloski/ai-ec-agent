from typing import Optional, List

from common.mixins.json_serializable import JSONSerializable


class PageCopyDto(JSONSerializable):

    def __init__(
        self,
        id: int,
        page_content_plan_id: Optional[int],
        sections: Optional[List[dict]],
    ):
        self.id = id
        self.page_content_plan_id = page_content_plan_id
        self.sections = sections

    def to_dict(self, exclude=None):
        exclude = set(exclude or [])

        data = {
            "id": self.id,
            "page_content_plan_id": self.page_content_plan_id,
            "sections": self.sections,
        }

        return {k: v for k, v in data.items() if k not in exclude}
