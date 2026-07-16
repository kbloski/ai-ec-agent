from typing import List

from sqlalchemy.orm import Session

from domain.models.advertisement.advertisement_visualization import AdvertisementVisualization
from infrastructure.logging.logger import Logger


class AdvertisementVisualizationsRepository:
    def __init__(self, logger: Logger, db: Session):
        self.logger = logger
        self.db = db

    # ➕ CREATE
    def create(self, item: AdvertisementVisualization) -> AdvertisementVisualization:
        self.db.add(item)
        self.db.commit()
        self.db.refresh(item)
        return item

    # ➕ CREATE MANY
    def create_many(
        self, items: List[AdvertisementVisualization]
    ) -> List[AdvertisementVisualization]:
        if not items:
            return []

        self.db.add_all(items)
        self.db.commit()

        for item in items:
            self.db.refresh(item)

        return items

    # 🔍 FIND FOR ADVERTISEMENT
    def find_for_advertisement(
        self, advertisement_id: int
    ) -> List[AdvertisementVisualization]:
        return (
            self.db.query(AdvertisementVisualization)
            .filter(AdvertisementVisualization.advertisement_id == advertisement_id)
            .all()
        )
