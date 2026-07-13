from typing import Dict, Any
from di.container import Container
from application.mappers.target_audience_mapper import TargetAudienceMapper

def get_target_audience_handler( knowledge_id: int) -> Dict[str, Any]:
    container = Container()

    target_audiences_repository = container.target_audiences_repository()
    
    items_db = target_audiences_repository.find_for_knowledge(knowledge_id)

    return [TargetAudienceMapper.to_dto(t) for t in items_db]
