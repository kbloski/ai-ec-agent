from sqlalchemy import Column, Integer, DateTime, ForeignKey, JSON
from sqlalchemy.sql import func

from infrastructure.database.db import Base
from common.mixins.json_serializable import JSONSerializable
from domain.enums.table_name import TableName


class PageCopy(Base, JSONSerializable):

    __tablename__ = TableName.PAGE_COPY.value

    # primary key
    id = Column(Integer, primary_key=True, autoincrement=True)

    page_content_plan_id = Column(
        Integer,
        ForeignKey(TableName.PAGE_CONTENT_PLAN + ".id", ondelete="CASCADE"),
        nullable=True
    )

    sections = Column(JSON, nullable=True)

    # timestamps
    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now()
    )

    updated_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now()
    )
