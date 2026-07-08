from sqlalchemy import Column, Integer, String, Text, JSON, DateTime, ForeignKey
from sqlalchemy.sql import func

from common.mixins.json_serializable import JSONSerializable
from infrastructure.database.db import Base
from domain.enums.table_name import TableName


class KnowledgeAnalysis(Base, JSONSerializable):
    __tablename__ = TableName.KNOWLEDGE_ANALYSES

    id = Column(Integer, primary_key=True, autoincrement=True)

    knowledge_id = Column(
        Integer,
        ForeignKey(TableName.KNOWLEDGES + ".id", ondelete="CASCADE"),
        nullable=False
    )

    # Prompt / instrukcja według której AI wykonało analizę
    # instruction = Column(Text, nullable=False)

    # Wynik wygenerowany przez AI
    # result = Column(Text, nullable=False)

    # Opcjonalne metadane analizy
    # metadata = Column(JSON, nullable=True)

    # np. model AI, wersja promptu, czas wykonania
    # model = Column(String, nullable=True)

    # recommendation = Column(
    #     Enum(AnalysisRecommendation),
    #     nullable=False
    # )

    assessment_status = Column(Text, nullable=False)

    recommendation_score = Column(Integer, nullable=False)

    summary = Column(Text, nullable=False)

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now()
    )