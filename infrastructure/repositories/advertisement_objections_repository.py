from typing import List

from sqlalchemy.orm import Session

from domain.models.advertisement.advertisement_objection import AdvertisementObjection
from infrastructure.logging.logger import Logger


class AdvertisementObjectionsRepository:
    def __init__(self, logger: Logger, db: Session):
        self.logger = logger
        self.db = db

    # ➕ CREATE
    def create(self, item: AdvertisementObjection) -> AdvertisementObjection:
        self.db.add(item)
        self.db.commit()
        self.db.refresh(item)
        return item

    # ➕ CREATE MANY
    def create_many(
        self, items: List[AdvertisementObjection]
    ) -> List[AdvertisementObjection]:
        if not items:
            return []

        self.db.add_all(items)
        self.db.commit()

        for item in items:
            self.db.refresh(item)

        return items

    # 🔍 FIND FOR ADVERTISEMENT
    def find_for_advertisement(self, advertisement_id: int) -> List[AdvertisementObjection]:
        return (
            self.db.query(AdvertisementObjection)
            .filter(AdvertisementObjection.advertisement_id == advertisement_id)
            .all()
        )
