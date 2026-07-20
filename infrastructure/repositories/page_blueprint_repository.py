from typing import List, Optional

from sqlalchemy.orm import Session

from domain.models.page_blueprint.page_blueprint import PageBlueprint
from infrastructure.logging.logger import Logger


class PageBlueprintRepository:
    def __init__(self, logger: Logger, db: Session):
        self.logger = logger
        self.db = db

    # ➕ CREATE
    def create(self, item: PageBlueprint) -> PageBlueprint:
        self.db.add(item)
        self.db.commit()
        self.db.refresh(item)
        return item

    # 🔍 GET BY ID
    def get_by_id(self, id: int) -> Optional[PageBlueprint]:
        return self.db.query(PageBlueprint).filter(PageBlueprint.id == id).first()

    # 🔍 GET BY PAGE STRATEGY ID
    def get_by_page_strategy_id(self, page_strategy_id: int) -> List[PageBlueprint]:
        return (
            self.db.query(PageBlueprint)
            .filter(PageBlueprint.page_strategy_id == page_strategy_id)
            .all()
        )
