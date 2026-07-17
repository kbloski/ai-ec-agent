from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, JSON
from sqlalchemy.sql import func

from infrastructure.database.db import Base
from common.mixins.json_serializable import JSONSerializable
from domain.enums.table_name import TableName


class AdExecution(Base, JSONSerializable):

    __tablename__ = TableName.AD_EXECUTION.value

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

    creative_strategy_id = Column(
        Integer,
        ForeignKey(TableName.CREATIVE_STRATEGY + ".id"),
        nullable=False
    )

    name = Column(String, nullable=True)

    execution = Column(JSON, nullable=True)
    hook_strategy = Column(JSON, nullable=True)
    structure = Column(JSON, nullable=True)
    scenes = Column(JSON, nullable=True)
    asset_requirements = Column(JSON, nullable=True)
    production_notes = Column(JSON, nullable=True)
    cta = Column(JSON, nullable=True)

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
