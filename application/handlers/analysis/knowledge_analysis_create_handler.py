from di.container import Container
from domain.models.analysis.analysis import Analysis
from domain.models.analysis.knowledge_analysis import KnowledgeAnalysis


def knowledge_analysis_create_handler(knowledge_id: int):
    container = Container()
    analysis_repository = container.analysis_repository()
    knowledge_analysis_repotistory = container.knowledge_analysis_repository()

    analysis = Analysis()

    # zapisanie analizy (zakładam, że masz repozytorium w kontenerze)
    analysis = analysis_repository.create(analysis)

    new_knowledge_analysis = KnowledgeAnalysis(
        knowledge_id=knowledge_id,
        analysis_id=analysis.id
    )

    new_knowledge_analysis =  knowledge_analysis_repotistory.upsert(new_knowledge_analysis)

    return new_knowledge_analysis