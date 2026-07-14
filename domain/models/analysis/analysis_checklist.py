from sqlalchemy import Column, Integer, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from common.mixins.json_serializable import JSONSerializable
from infrastructure.database.db import Base
from domain.enums.table_name import TableName


class AnalysisChecklist(Base, JSONSerializable):
    __tablename__ = TableName.ANALYSIS_CHECKLIST

    id = Column(Integer, primary_key=True, autoincrement=True)

    analysis_id = Column(
        Integer,
        ForeignKey(f"{TableName.ANALYSIS}.id"),
        nullable=False
    )

    checklist_id = Column(
        Integer,
        ForeignKey(f"{TableName.CHECKLIST}.id"),
        nullable=False
    )

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now()
    )