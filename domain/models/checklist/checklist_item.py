from sqlalchemy import Column, Integer, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from common.mixins.json_serializable import JSONSerializable
from infrastructure.database.db import Base
from domain.enums.table_name import TableName


class ChecklistItem(Base, JSONSerializable):
    __tablename__ = TableName.CHECKLIST_ITEM

    id = Column(Integer, primary_key=True, autoincrement=True)

    checklist_id = Column(
        Integer,
        ForeignKey(f"{TableName.CHECKLIST.value}.id"),
        nullable=False
    )

    question = Column(Text, nullable=False)
    answer= Column(Text, nullable=True)
    notes = Column(Text, nullable=True)

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now()
    )