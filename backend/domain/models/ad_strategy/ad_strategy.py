from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, JSON
from sqlalchemy.sql import func

from infrastructure.database.db import Base
from common.mixins.json_serializable import JSONSerializable
from domain.enums.table_name import TableName


class AdStrategy(Base, JSONSerializable):

    __tablename__ = TableName.AD_STRATEGY.value

    # primary key
    id = Column(Integer, primary_key=True, autoincrement=True)

    # relations
    message_strategy_id = Column(
        Integer,
        ForeignKey(TableName.MESSAGE_STRATEGY + ".id", ondelete="CASCADE"),
        nullable=False
    )

    objective = Column(JSON, nullable=True)
    customer_stage = Column(String, nullable=True)

    priority_audiences = Column(JSON, nullable=True)
    audience_angles = Column(JSON, nullable=True)
    message_angles = Column(JSON, nullable=True)
    offer_angles = Column(JSON, nullable=True)
    creative_concepts = Column(JSON, nullable=True)
    recommended_formats = Column(JSON, nullable=True)
    testing_hypotheses = Column(JSON, nullable=True)

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
