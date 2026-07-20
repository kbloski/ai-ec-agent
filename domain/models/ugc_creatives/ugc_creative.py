from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, JSON
from sqlalchemy.sql import func

from infrastructure.database.db import Base
from common.mixins.json_serializable import JSONSerializable
from domain.enums.table_name import TableName


class UgcCreative(Base, JSONSerializable):

    __tablename__ = TableName.UGC_CREATIVES.value

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

    name = Column(String, nullable=True)
    customer_persona = Column(JSON, nullable=True)
    content_format = Column(String, nullable=True)
    angle = Column(String, nullable=True)
    hook_idea = Column(String, nullable=True)
    video_flow = Column(JSON, nullable=True)
    recording_style = Column(String, nullable=True)
    platform_fit = Column(JSON, nullable=True)
    cta = Column(String, nullable=True)
    why_it_should_work = Column(String, nullable=True)

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
