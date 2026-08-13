from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Float, Index, Boolean
from sqlalchemy.sql import func

from infrastructure.database.db import Base
from common.mixins.json_serializable import JSONSerializable
from domain.enums.table_name import TableName


class OfferInsight(Base, JSONSerializable):
    __tablename__ = TableName.OFFER_INSIGHTS.value

    # Primary key
    id = Column(Integer, primary_key=True, autoincrement=True)

    # Relation to offer
    offer_id = Column(
        Integer,
        ForeignKey(TableName.OFFERS + ".id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    type = Column(String(50), nullable=False, index=True)

    fact_status = Column(String(20), nullable=False, index=True)

    # optional scoring (AI confidence / business importance)
    # score = Column(Float, nullable=True)

    # Actual insight value
    value = Column(String, nullable=False)

    #uzasadnienie 
    # evidence = Column(String, nullable=True)

    is_favorite = Column(Boolean, nullable=False, default=False, server_default="0")

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
        Index("ix_offer_insight_offer_type_fact_status", "offer_id", "type", "fact_status"),
    )
