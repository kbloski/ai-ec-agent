from typing import List, Optional

from sqlalchemy.orm import Session

from domain.models.advertisement.scene import Scene
from infrastructure.logging.logger import Logger


class ScenesRepository:
    def __init__(self, logger: Logger, db: Session):
        self.logger = logger
        self.db = db

    # ➕ CREATE
    def create(self, item: Scene) -> Scene:
        self.db.add(item)
        self.db.commit()
        self.db.refresh(item)
        return item

    # ➕ CREATE MANY
    def create_many(self, items: List[Scene]) -> List[Scene]:
        if not items:
            return []

        self.db.add_all(items)
        self.db.commit()

        for item in items:
            self.db.refresh(item)

        return items

    # 🔍 GET BY ID
    def get_by_id(self, id: int) -> Optional[Scene]:
        return self.db.query(Scene).filter(Scene.id == id).first()
