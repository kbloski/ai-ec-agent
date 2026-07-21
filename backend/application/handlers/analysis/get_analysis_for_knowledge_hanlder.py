from di.container import Container
from application.mappers.analysis_mapper import AnalysisMapper

def get_analysis_for_knowledge_handler(knowledge_id : int):
    container = Container()

    knowledge_analysis_repository = container.knowledge_analysis_repository()
    analysis_repository = container.analysis_repository()

    knowledge_analysis_db = knowledge_analysis_repository.find_by_knowledge_id(knowledge_id=knowledge_id)
    knowledge_analysis_ids = [k.analysis_id for k in knowledge_analysis_db]

    analysis_db = analysis_repository.get_by_ids(ids=knowledge_analysis_ids)
    analysis_dtos = [AnalysisMapper.to_dto(a) for a in analysis_db]

    return analysis_dtos