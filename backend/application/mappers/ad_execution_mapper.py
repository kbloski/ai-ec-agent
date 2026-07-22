from domain.models.ad_execution.ad_execution import AdExecution
from application.dtos.ad_execution.ad_execution_response_dto import AdExecutionDto


class AdExecutionMapper:

    @staticmethod
    def to_dto(item: AdExecution) -> AdExecutionDto:
        return AdExecutionDto(
            id=item.id,
            creative_strategy_id=item.creative_strategy_id,
            name=item.name,
            creative_type=item.creative_type,
            platform=item.platform,
            format=item.format,
        )
