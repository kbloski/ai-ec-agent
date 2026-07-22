from domain.models.ad_execution.ad_execution import AdExecution
from application.dtos.ad_execution.ad_execution_response_dto import AdExecutionDto


class AdExecutionMapper:

    @staticmethod
    def to_dto(item: AdExecution) -> AdExecutionDto:
        return AdExecutionDto(
            id=item.id,
            creative_strategy_id=item.creative_strategy_id,
            name=item.name,
            execution=item.execution,
            hook_strategy=item.hook_strategy,
            structure=item.structure,
            scenes=item.scenes,
            asset_requirements=item.asset_requirements,
            production_notes=item.production_notes,
            cta=item.cta,
        )
