from domain.models.experiment.experiment import Experiment
from application.dtos.experiment.experiment_response_dto import ExperimentDto


class ExperimentMapper:

    @staticmethod
    def to_dto(item: Experiment) -> ExperimentDto:
        return ExperimentDto(
            id=item.id,
            knowledge_id=item.knowledge_id,
            name=item.name,
            description=item.description,
            experiment_type=item.experiment_type,
            framework=item.framework,
            angle=item.angle,
            psychology_trigger=item.psychology_trigger,
            awareness_stage=item.awareness_stage,
            hypothesis=item.hypothesis,
            expected_result=item.expected_result,
            primary_problem=item.primary_problem,
            primary_desire=item.primary_desire,
            primary_fear=item.primary_fear,
            dream_outcome=item.dream_outcome,
            big_idea=item.big_idea,
            big_promise=item.big_promise,
            unique_mechanism=item.unique_mechanism,
            core_message=item.core_message,
            offer_strategy=item.offer_strategy,
            urgency_strategy=item.urgency_strategy,
            cta_strategy=item.cta_strategy,
            proof_strategy=item.proof_strategy,
            priority=item.priority,
            confidence=item.confidence,
            status=item.status,
            notes=item.notes,
        )

    @staticmethod
    def to_entity(knowledge_id: int, data: dict) -> Experiment:
        return Experiment(
            knowledge_id=knowledge_id,
            name=data.get("name", ""),
            description=data.get("description"),
            experiment_type=data.get("experiment_type"),
            framework=data.get("framework"),
            angle=data.get("angle"),
            psychology_trigger=data.get("psychology_trigger"),
            awareness_stage=data.get("awareness_stage"),
            hypothesis=data.get("hypothesis"),
            expected_result=data.get("expected_result"),
            primary_problem=data.get("primary_problem"),
            primary_desire=data.get("primary_desire"),
            primary_fear=data.get("primary_fear"),
            dream_outcome=data.get("dream_outcome"),
            big_idea=data.get("big_idea"),
            big_promise=data.get("big_promise"),
            unique_mechanism=data.get("unique_mechanism"),
            core_message=data.get("core_message"),
            offer_strategy=data.get("offer_strategy"),
            urgency_strategy=data.get("urgency_strategy"),
            cta_strategy=data.get("cta_strategy"),
            proof_strategy=data.get("proof_strategy"),
            priority=data.get("priority"),
            confidence=data.get("confidence"),
            status=data.get("status", "DRAFT"),
            notes=data.get("notes"),
        )
