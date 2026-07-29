from typing import Any, Dict

from di.container import Container
from application.mappers.marketing_strategy_mapper import MarketingStrategyMapper

DENYLIST = {"id", "brand_marketing_id", "created_at", "updated_at"}


def update_marketing_strategy_handler(id: int, fields: Dict[str, Any]):
    container = Container()
    marketing_strategy_repository = container.marketing_strategy_repository()

    item = marketing_strategy_repository.get_by_id(id)

    for key, value in fields.items():
        if key not in DENYLIST:
            setattr(item, key, value)

    updated = marketing_strategy_repository.update(item)
    return MarketingStrategyMapper.to_dto(updated).to_dict()
