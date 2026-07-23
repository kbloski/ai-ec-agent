from sqlalchemy.orm import Session
from typing import List, Optional

from domain.models.analysis.question_answer import QuestionAnswer
from infrastructure.logging.logger import Logger

class QuestionAnswerRepository:
    def __init__(self, logger: Logger, db: Session):
        self.logger = logger
        self.db = db

    # ➕ CREATE MANY
    def create_many(
        self,
        items: list[QuestionAnswer]
    ) -> list[QuestionAnswer]:

        if not items:
            return []

        self.db.add_all(items)
        self.db.commit()

        for item in items:
            self.db.refresh(item)

        return items

    # 🔍 GET BY ID
    def get_by_id(self, id: int) -> Optional[QuestionAnswer]:
        return self.db.query(QuestionAnswer).filter(QuestionAnswer.id == id).first()

    # 🔍 GET BY IDS
    def get_by_ids(self, ids: List[int]) -> List[QuestionAnswer]:
        return (
            self.db.query(QuestionAnswer)
            .filter(QuestionAnswer.id.in_(ids))
            .all()
        )

    # ❌ DELETE
    def delete(self, id: int) -> bool:
        item = self.db.query(QuestionAnswer).filter(QuestionAnswer.id == id).first()

        if not item:
            return False

        self.db.delete(item)
        self.db.commit()
        return True
