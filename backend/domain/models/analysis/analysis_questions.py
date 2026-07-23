from sqlalchemy import Column, Integer, Text, DateTime, ForeignKey, Float, JSON
from sqlalchemy.sql import func

from common.mixins.json_serializable import JSONSerializable
from infrastructure.database.db import Base
from domain.enums.table_name import TableName


class AnalysisQuestion(Base, JSONSerializable):
    __tablename__ = TableName.ANALYSIS_QUESTIONS.value

    id = Column(
        Integer,
        primary_key=True,
        autoincrement=True
    )

    analysis_id = Column(
        Integer,
        ForeignKey("analysis.id", ondelete="CASCADE"),
        nullable=False
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