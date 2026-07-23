from sqlalchemy import Column, Integer, Text, DateTime, Float
from sqlalchemy.sql import func

from common.mixins.json_serializable import JSONSerializable
from infrastructure.database.db import Base
from domain.enums.table_name import TableName


class QuestionAnswer(Base, JSONSerializable):
    __tablename__ = TableName.QUESTION_ANSWERS.value

    id = Column(
        Integer,
        primary_key=True,
        autoincrement=True
    )

    question = Column(
        Text,
        nullable=False
    )

    answer = Column(
        Text,
        nullable=True
    )

    # Ocena jakości odpowiedzi 1-10
    score = Column(
        Integer,
        nullable=True
    )

    # Pewność AI np. 0.92
    confidence = Column(
        Float,
        nullable=True
    )

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now()
    )
