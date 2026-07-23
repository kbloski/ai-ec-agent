from domain.models.creative_execution.creative_execution import CreativeExecution
from application.dtos.creative_execution.creative_execution_response_dto import CreativeExecutionDto


class CreativeExecutionMapper:

    @staticmethod
    def to_dto(item: CreativeExecution) -> CreativeExecutionDto:
        return CreativeExecutionDto(
            id=item.id,
            ad_execution_id=item.ad_execution_id,
            content_json=item.content_json,
        )
