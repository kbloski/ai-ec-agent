from enum import Enum

class DecisionTime(str, Enum):
    IMMEDIATE = "immediate"
    DAYS = "days"
    WEEKS = "weeks"
    MONTHS = "months"