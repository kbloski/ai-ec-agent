from di.container import Container
from application.mappers.knowledge_insight_mapper import KnowledgeInsightMapper


def get_knowledge_insight_handler(id: int):
    container = Container()
    knowledge_insights_repository = container.knowledge_insights_repository()

    item = knowledge_insights_repository.get_by_id(id)
    return KnowledgeInsightMapper.to_dto(item).to_dict()
