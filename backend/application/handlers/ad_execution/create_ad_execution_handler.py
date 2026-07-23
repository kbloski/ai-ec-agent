from di.container import Container

from domain.models.ad_execution.ad_execution import AdExecution
from domain.enums.enums import CreativeTypes

ALLOWED_CREATIVE_TYPES = [item.value for item in CreativeTypes]


def create_ad_execution_handler(
    creative_strategy_id: int,
    creative_type: str,
    platform: str,
    format: str,
    name: str | None = None
):

    if creative_type not in ALLOWED_CREATIVE_TYPES:
        raise ValueError(
            f"Unsupported creative type: {creative_type}"
        )


    container = Container()


    ad_execution_service = (
        container.ad_execution_service()
    )


    entity = AdExecution(

        creative_strategy_id=creative_strategy_id,

        name=name or (
            f"{creative_type.capitalize()} Ad Execution"
        ),

        creative_type=creative_type,

        platform=platform,

        format=format

    )


    return ad_execution_service.create_ad_execution(entity)
