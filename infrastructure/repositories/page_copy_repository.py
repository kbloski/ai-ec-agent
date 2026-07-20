from typing import List, Optional

from sqlalchemy.orm import Session

from domain.models.page_copy.page_copy import PageCopy
from infrastructure.logging.logger import Logger


class PageCopyRepository:
    def __init__(self, logger: Logger, db: Session):
        self.logger = logger
        self.db = db

    # ➕ CREATE
    def create(self, item: PageCopy) -> PageCopy:
        self.db.add(item)
        self.db.commit()
        self.db.refresh(item)
        return item

    # 🔍 GET BY ID
    def get_by_id(self, id: int) -> Optional[PageCopy]:
        return self.db.query(PageCopy).filter(PageCopy.id == id).first()

    # 🔍 GET BY PAGE CONTENT PLAN ID
    def get_by_page_content_plan_id(self, page_content_plan_id: int) -> List[PageCopy]:
        return (
            self.db.query(PageCopy)
            .filter(PageCopy.page_content_plan_id == page_content_plan_id)
            .all()
        )
