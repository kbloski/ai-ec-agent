from typing import Dict, Any
from di.container import Container
from application.mappers.target_audience_mapper import TargetAudienceMapper

def get_target_audience_preview_handler( target_audience_id: int) -> Dict[str, Any]:
    container = Container()
    repo = container.target_audiences_repository()
    assember = container.target_audience_assembler()

    target_audience_db =repo.find_by_id(target_audience_id)
    dto = TargetAudienceMapper.to_dto( target_audience_db )
    assembled_dto = assember.assemble_dto(dto)
    return assembled_dto