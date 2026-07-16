from typing import Optional

from common.mixins.json_serializable import JSONSerializable


class ExperimentDto(JSONSerializable):

    def __init__(
        self,
        id: int,
        knowledge_id: int,
        name: str,
        description: Optional[str],
        experiment_type: Optional[str],
        framework: Optional[str],
        angle: Optional[str],
        psychology_trigger: Optional[str],
        awareness_stage: Optional[str],
        hypothesis: Optional[str],
        expected_result: Optional[str],
        primary_problem: Optional[str],
        primary_desire: Optional[str],
        primary_fear: Optional[str],
        dream_outcome: Optional[str],
        big_idea: Optional[str],
        big_promise: Optional[str],
        unique_mechanism: Optional[str],
        core_message: Optional[str],
        offer_strategy: Optional[str],
        urgency_strategy: Optional[str],
        cta_strategy: Optional[str],
        proof_strategy: Optional[str],
        priority: Optional[int],
        confidence: Optional[int],
        status: Optional[str],
        notes: Optional[str],
    ):
        self.id = id
        self.knowledge_id = knowledge_id
        self.name = name
        self.description = description
        self.experiment_type = experiment_type
        self.framework = framework
        self.angle = angle
        self.psychology_trigger = psychology_trigger
        self.awareness_stage = awareness_stage
        self.hypothesis = hypothesis
        self.expected_result = expected_result
        self.primary_problem = primary_problem
        self.primary_desire = primary_desire
        self.primary_fear = primary_fear
        self.dream_outcome = dream_outcome
        self.big_idea = big_idea
        self.big_promise = big_promise
        self.unique_mechanism = unique_mechanism
        self.core_message = core_message
        self.offer_strategy = offer_strategy
        self.urgency_strategy = urgency_strategy
        self.cta_strategy = cta_strategy
        self.proof_strategy = proof_strategy
        self.priority = priority
        self.confidence = confidence
        self.status = status
        self.notes = notes

    def to_dict(self, exclude=None):
        exclude = set(exclude or [])

        data = {
            "id": self.id,
            "knowledge_id": self.knowledge_id,
            "name": self.name,
            "description": self.description,
            "experiment_type": self.experiment_type,
            "framework": self.framework,
            "angle": self.angle,
            "psychology_trigger": self.psychology_trigger,
            "awareness_stage": self.awareness_stage,
            "hypothesis": self.hypothesis,
            "expected_result": self.expected_result,
            "primary_problem": self.primary_problem,
            "primary_desire": self.primary_desire,
            "primary_fear": self.primary_fear,
            "dream_outcome": self.dream_outcome,
            "big_idea": self.big_idea,
            "big_promise": self.big_promise,
            "unique_mechanism": self.unique_mechanism,
            "core_message": self.core_message,
            "offer_strategy": self.offer_strategy,
            "urgency_strategy": self.urgency_strategy,
            "cta_strategy": self.cta_strategy,
            "proof_strategy": self.proof_strategy,
            "priority": self.priority,
            "confidence": self.confidence,
            "status": self.status,
            "notes": self.notes,
        }

        return {k: v for k, v in data.items() if k not in exclude}
