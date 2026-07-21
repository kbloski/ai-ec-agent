from typing import List, Optional

from sqlalchemy.orm import Session

from domain.models.page_content_plan.page_content_plan import PageContentPlan
from infrastructure.logging.logger import Logger


class PageContentPlanRepository:
    def __init__(self, logger: Logger, db: Session):
        self.logger = logger
        self.db = db

    # ➕ CREATE
    def create(self, item: PageContentPlan) -> PageContentPlan:
        self.db.add(item)
        self.db.commit()
        self.db.refresh(item)
        return item

    # 🔍 GET BY ID
    def get_by_id(self, id: int) -> Optional[PageContentPlan]:
        return self.db.query(PageContentPlan).filter(PageContentPlan.id == id).first()

    # 🔍 GET BY PAGE BLUEPRINT ID
    def get_by_page_blueprint_id(self, page_blueprint_id: int) -> List[PageContentPlan]:
        return (
            self.db.query(PageContentPlan)
            .filter(PageContentPlan.page_blueprint_id == page_blueprint_id)
            .all()
        )

    # ❌ DELETE
    def delete(self, id: int) -> bool:
        item = self.db.query(PageContentPlan).filter(PageContentPlan.id == id).first()

        if not item:
            return False

        self.db.delete(item)
        self.db.commit()
        return True
