from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.sql import func

from infrastructure.database.db import Base
from common.mixins.json_serializable import JSONSerializable
from domain.enums.table_name import TableName


class AdExecution(Base, JSONSerializable):

    __tablename__ = TableName.AD_EXECUTION.value

    # primary key
    id = Column(Integer, primary_key=True, autoincrement=True)

    # relations
    creative_strategy_id = Column(
        Integer,
        ForeignKey(TableName.CREATIVE_STRATEGY + ".id", ondelete="CASCADE"),
        nullable=False
    )

    name = Column(String, nullable=True)

    creative_type = Column(String, nullable=False)
    platform = Column(String, nullable=True)
    format = Column(String, nullable=True)

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
