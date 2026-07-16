from typing import List, Optional

from sqlalchemy.orm import Session

from domain.models.advertisement.advertisement import Advertisement
from infrastructure.logging.logger import Logger


class AdvertisementsRepository:
    def __init__(self, logger: Logger, db: Session):
        self.logger = logger
        self.db = db

    # ➕ CREATE
    def create(self, item: Advertisement) -> Advertisement:
        self.db.add(item)
        self.db.commit()
        self.db.refresh(item)
        return item

    # 🔍 GET BY ID
    def get_by_id(self, id: int) -> Optional[Advertisement]:
        return self.db.query(Advertisement).filter(Advertisement.id == id).first()

    # 🔍 GET BY KNOWLEDGE ID
    def get_by_knowledge_id(self, knowledge_id: int) -> List[Advertisement]:
        return (
            self.db.query(Advertisement)
            .filter(Advertisement.knowledge_id == knowledge_id)
            .all()
        )
