from enum import Enum


class PageSectionRequirementType(str, Enum):
    REQUIRED = "required"
    OPTIONAL = "optional"
    EXCLUDED = "excluded"
