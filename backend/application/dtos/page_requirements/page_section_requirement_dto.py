from typing import Optional

from common.mixins.json_serializable import JSONSerializable


class PageSectionRequirementDto(JSONSerializable):
    def __init__(
        self,
        id: int,
        page_requirements_id: int,
        page_section_type_id: str,
        requirement_type: str,
        position: Optional[int],
    ):
        self.id = id
        self.page_requirements_id = page_requirements_id
        self.page_section_type_id = page_section_type_id
        self.requirement_type = requirement_type
        self.position = position

    def to_dict(self, exclude=None):
        exclude = set(exclude or [])

        data = {
            "id": self.id,
            "page_requirements_id": self.page_requirements_id,
            "page_section_type_id": self.page_section_type_id,
            "requirement_type": self.requirement_type,
            "position": self.position,
        }

        return {k: v for k, v in data.items() if k not in exclude}

    def to_content_dict(self):
        return {
            "page_section_type_id": self.page_section_type_id,
            "requirement_type": self.requirement_type,
            "position": self.position,
        }
