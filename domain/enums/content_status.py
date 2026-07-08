from enum import Enum

class ContentStatus(str, Enum):
    APPROVED = "approved"
    SUGGESTED = "suggested"
    REJECTED = "rejected"