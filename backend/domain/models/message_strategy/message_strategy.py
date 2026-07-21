from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, JSON
from sqlalchemy.sql import func

from infrastructure.database.db import Base
from common.mixins.json_serializable import JSONSerializable
from domain.enums.table_name import TableName


class MessageStrategy(Base, JSONSerializable):

    __tablename__ = TableName.MESSAGE_STRATEGY.value

    # primary key
    id = Column(Integer, primary_key=True, autoincrement=True)

    # relations
    knowledge_id = Column(
        Integer,
        ForeignKey("knowledge.id"),
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

    core_message = Column(Text, nullable=True)
    brand_message = Column(Text, nullable=True)

    primary_message_angle = Column(Text, nullable=True)
    secondary_message_angles = Column(JSON, nullable=True)

    audience_messages = Column(JSON, nullable=True)

    customer_pain_points = Column(JSON, nullable=True)
    customer_desires = Column(JSON, nullable=True)

    benefit_messages = Column(JSON, nullable=True)
    feature_to_benefit_mapping = Column(JSON, nullable=True)

    objection_handling_messages = Column(JSON, nullable=True)
    trust_messages = Column(JSON, nullable=True)
    proof_points = Column(JSON, nullable=True)

    emotional_triggers = Column(JSON, nullable=True)
    rational_arguments = Column(JSON, nullable=True)

    advertising_angles = Column(JSON, nullable=True)
    content_angles = Column(JSON, nullable=True)
    ugc_angles = Column(JSON, nullable=True)

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
