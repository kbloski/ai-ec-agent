from sqlalchemy import Column, Integer, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from common.mixins.json_serializable import JSONSerializable
from infrastructure.database.db import Base
from domain.enums.table_name import TableName


class AnalysisChecklist(Base, JSONSerializable):
    __tablename__ = TableName.ANALYSIS_CHECKLIST

    analysis_id = Column(
        Integer,
        ForeignKey(f"{TableName.ANALYSIS}.id"),
        nullable=False,
        primary_key=True
    )

    checklist_id = Column(
        Integer,
        ForeignKey(f"{TableName.CHECKLIST}.id"),
        nullable=False,
        primary_key=True
    )
