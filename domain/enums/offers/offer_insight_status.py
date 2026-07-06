from enum import Enum

class OfferInsightStatus(str, Enum):
    APPROVED = "approved"
    SUGGESTED = "suggested"
    REJECTED = "rejected"