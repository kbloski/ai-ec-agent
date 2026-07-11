from enum import Enum

class KnowledgeInsightType(str, Enum):
    PROBLEM_SOLVED = "problem_solved"
    SOLUTION = "solution"
    TRANSFORMATION = "transformation"

    OFFER_COMPONENT = "offer_component"

    FEATURE = "feature"
    FUNCTIONAL_BENEFIT = "functional_benefit"
    EMOTIONAL_BENEFIT = "emotional_benefit"

    VALUE_PROPOSITION = "value_proposition"

    DIFFERENTIATOR = "differentiator"

    STRENGTH = "strength"
    LIMITATION = "limitation"

    ASSUMPTION = "assumption"

    ADDITIONAL_INSIGHT = "additional_insight"
