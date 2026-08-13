from di.container import Container
from application.mappers.knowledge_insight_mapper import KnowledgeInsightMapper
from domain.enums.fact_status import FactStatus
from domain.enums.review_status import ReviewStatus


def update_knowledge_insight_handler(
    id: int,
    fact_status: str | None = None,
    review_status: str | None = None,
):
    container = Container()
    knowledge_insights_repository = container.knowledge_insights_repository()

    item = knowledge_insights_repository.get_by_id(id)
    if item is None:
        raise ValueError(f"Knowledge insight {id} not found")
    if fact_status is not None:
        item.fact_status = FactStatus(fact_status).value
    if review_status is not None:
        item.review_status = ReviewStatus(review_status).value

    updated = knowledge_insights_repository.update(item)
    return KnowledgeInsightMapper.to_dto(updated).to_dict()
