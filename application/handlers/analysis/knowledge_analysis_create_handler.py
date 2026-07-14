from di.container import Container
from domain.models.analysis.analysis import Analysis
from domain.models.analysis.knowledge_analysis import KnowledgeAnalysis
from application.mappers.analysis_mapper import AnalysisMapper

def knowledge_analysis_create_handler(knowledge_id: int):
    container = Container()
    analysis_repository = container.analysis_repository()
    knowledge_analysis_repotistory = container.knowledge_analysis_repository()

    new_analysis = Analysis()

    # zapisanie analizy (zakładam, że masz repozytorium w kontenerze)
    new_analysis = analysis_repository.create(new_analysis)

    new_knowledge_analysis = KnowledgeAnalysis(
        knowledge_id=knowledge_id,
        analysis_id=new_analysis.id
    )

    new_knowledge_analysis =  knowledge_analysis_repotistory.upsert(new_knowledge_analysis)

    return AnalysisMapper.to_dto(new_analysis) 