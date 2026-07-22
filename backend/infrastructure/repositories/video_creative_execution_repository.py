from typing import List, Optional

from sqlalchemy.orm import Session

from domain.models.video_creative_execution.video_creative_execution import VideoCreativeExecution
from infrastructure.logging.logger import Logger


class VideoCreativeExecutionRepository:
    def __init__(self, logger: Logger, db: Session):
        self.logger = logger
        self.db = db

    # ➕ CREATE
    def create(self, item: VideoCreativeExecution) -> VideoCreativeExecution:
        self.db.add(item)
        self.db.commit()
        self.db.refresh(item)
        return item

    # 🔍 GET BY ID
    def get_by_id(self, id: int) -> Optional[VideoCreativeExecution]:
        return self.db.query(VideoCreativeExecution).filter(VideoCreativeExecution.id == id).first()

    # 🔍 GET BY AD EXECUTION ID
    def get_by_ad_execution_id(self, ad_execution_id: int) -> List[VideoCreativeExecution]:
        return (
            self.db.query(VideoCreativeExecution)
            .filter(VideoCreativeExecution.ad_execution_id == ad_execution_id)
            .all()
        )

    # ❌ DELETE
    def delete(self, id: int) -> bool:
        item = self.db.query(VideoCreativeExecution).filter(VideoCreativeExecution.id == id).first()

        if not item:
            return False

        self.db.delete(item)
        self.db.commit()
        return True
