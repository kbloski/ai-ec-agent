from enum import Enum

class OfferInsightType(str, Enum):
    TARGET_AUDIENCE = "target_audience"
    PAIN_POINT = "pain_point"
    DESIRE = "desire"
    OBJECTION = "objection"
    