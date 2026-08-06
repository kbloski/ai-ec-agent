from sqlalchemy import Column, Integer, DateTime, ForeignKey, JSON, Boolean
from sqlalchemy.sql import func

from infrastructure.database.db import Base
from common.mixins.json_serializable import JSONSerializable
from domain.enums.table_name import TableName


class CreativeExecution(Base, JSONSerializable):

    __tablename__ = TableName.CREATIVE_EXECUTIONS.value

    # primary key
    id = Column(Integer, primary_key=True, autoincrement=True)

    # relations
    ad_execution_id = Column(
        Integer,
        ForeignKey(TableName.AD_EXECUTION + ".id", ondelete="CASCADE"),
        nullable=False
    )

    content_json = Column(JSON, nullable=False)

    is_favorite = Column(Boolean, nullable=False, default=False, server_default="0")

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
