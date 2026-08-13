from di.container import Container
from application.mappers.knowledge_insight_mapper import KnowledgeInsightMapper


def update_knowledge_insight_handler(id: int, fact_status: str):
    container = Container()
    knowledge_insights_repository = container.knowledge_insights_repository()

    item = knowledge_insights_repository.get_by_id(id)
    item.fact_status = fact_status

    updated = knowledge_insights_repository.update(item)
    return KnowledgeInsightMapper.to_dto(updated).to_dict()
