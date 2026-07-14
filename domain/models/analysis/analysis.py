from sqlalchemy import Column, Integer, String, Text, JSON, DateTime, ForeignKey
from sqlalchemy.sql import func

from common.mixins.json_serializable import JSONSerializable
from infrastructure.database.db import Base
from domain.enums.table_name import TableName


class Analysis(Base, JSONSerializable):
    __tablename__ = TableName.ANALYSIS.value

    id = Column(Integer, primary_key=True, autoincrement=True)

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now()
    )