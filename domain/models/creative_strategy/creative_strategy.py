from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, JSON
from sqlalchemy.sql import func

from infrastructure.database.db import Base
from common.mixins.json_serializable import JSONSerializable
from domain.enums.table_name import TableName


class CreativeStrategy(Base, JSONSerializable):

    __tablename__ = TableName.CREATIVE_STRATEGY.value

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

    message_strategy_id = Column(
        Integer,
        ForeignKey(TableName.MESSAGE_STRATEGY + ".id"),
        nullable=False
    )

    ad_strategy_id = Column(
        Integer,
        ForeignKey(TableName.AD_STRATEGY + ".id"),
        nullable=False
    )

    name = Column(String, nullable=True)
    based_on_ad_concept = Column(String, nullable=True)
    objective = Column(String, nullable=True)
    creative_type = Column(String, nullable=True)
    recommended_format = Column(String, nullable=True)
    platform = Column(String, nullable=True)
    duration = Column(String, nullable=True)
    aspect_ratio = Column(String, nullable=True)

    target = Column(JSON, nullable=True)
    hook_strategy = Column(JSON, nullable=True)
    story_framework = Column(JSON, nullable=True)
    creative_direction = Column(JSON, nullable=True)
    speaker = Column(JSON, nullable=True)
    emotion_flow = Column(JSON, nullable=True)
    visual_direction = Column(JSON, nullable=True)
    proof_strategy = Column(JSON, nullable=True)
    cta_strategy = Column(JSON, nullable=True)
    production_notes = Column(JSON, nullable=True)

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
