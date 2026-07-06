from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Float, Index
from sqlalchemy.sql import func

from infrastructure.database.db import Base
from common.mixins.json_serializable import JSONSerializable
from domain.enums.table_name import TableName


class OfferInsight(Base, JSONSerializable):
    __tablename__ = TableName.OFFER_INSIGHTS

    # Primary key
    id = Column(Integer, primary_key=True, autoincrement=True)

    # Relation to offer
    offer_id = Column(
        Integer,
        ForeignKey(TableName.OFFERS + ".id"),
        nullable=False,
        index=True,
    )

    # Type of insight
    # target_audience | pain_point | desire | objection
    type = Column(String(50), nullable=False, index=True)

    # Actual insight value
    value = Column(String, nullable=False)

    # draft | approved | rejected | archived
    status = Column(String(20), nullable=False, default="draft", index=True)

    # ai | manual
    source = Column(String(20), nullable=False, default="ai")

    # optional scoring (AI confidence / business importance)
    score = Column(Float, nullable=True)

    # timestamps
    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
    )

    updated_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
    )

    # useful composite index for queries
    __table_args__ = (
        Index("ix_offer_insight_offer_type_status", "offer_id", "type", "status"),
    )