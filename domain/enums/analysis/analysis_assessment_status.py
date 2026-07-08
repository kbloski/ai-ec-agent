from enum import Enum

class AnalysisAssessmentStatus(str, Enum):
    HIGH_POTENTIAL = "high_potential"
    MEDIUM_POTENTIAL = "medium_potential"
    LOW_POTENTIAL = "low_potential"
    REJECTED = "rejected"
    NEEDS_MORE_RESEARCH = "needs_more_research"