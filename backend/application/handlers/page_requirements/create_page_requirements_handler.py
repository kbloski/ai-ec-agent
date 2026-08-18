from di.container import Container
from domain.models.page_requirements.page_requirements import PageRequirements


def create_page_requirements_handler(page_strategy_id: int):
    container = Container()

    page_strategy_service = container.page_strategy_service()
    page_requirements_service = container.page_requirements_service()

    page_strategy_service.get_page_strategy_by_id(id=page_strategy_id)

    page_requirements = PageRequirements(page_strategy_id=page_strategy_id)

    return page_requirements_service.create_page_requirements(page_requirements)
