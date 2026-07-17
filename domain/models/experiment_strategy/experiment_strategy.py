from sqlalchemy import Column, Integer, Text, DateTime, ForeignKey, JSON
from sqlalchemy.sql import func

from infrastructure.database.db import Base
from common.mixins.json_serializable import JSONSerializable
from domain.enums.table_name import TableName


class ExperimentStrategy(Base, JSONSerializable):

    __tablename__ = TableName.EXPERIMENT_STRATEGY.value

    # primary key
    id = Column(Integer, primary_key=True, autoincrement=True)

    # relations
    knowledge_id = Column(
        Integer,
        ForeignKey(TableName.OFFER_KNOWLEDGE.value+".id"),
        nullable=False
    )

    brand_marketing_id = Column(
        Integer,
        ForeignKey(TableName.BRAND_MARKETING + ".id"),
        nullable=False
    )

    marketing_strategy_id = Column(
        Integer,
        ForeignKey(TableName.MARKETING_STRATEGY + ".id"),
        nullable=False
    )

    offer_strategy_id = Column(
        Integer,
        ForeignKey(TableName.OFFER_STRATEGY + ".id"),
        nullable=False
    )

    message_strategy_id = Column(
        Integer,
        ForeignKey(TableName.MESSAGE_STRATEGY + ".id"),
        nullable=False
    )

    experiment_strategy = Column(Text, nullable=True)
    learning_objectives = Column(JSON, nullable=True)

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
