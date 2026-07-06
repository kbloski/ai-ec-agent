from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, JSON
from sqlalchemy.sql import func

from infrastructure.database.db import Base
from common.mixins.json_serializable import JSONSerializable
from domain.enums.table_name import TableName


class OfferKnowledge(Base, JSONSerializable):
    __tablename__ = TableName.OFFER_UNDERSTANDINGS

    # Primary key
    id = Column(Integer, primary_key=True, autoincrement=True)

    # Related offer
    offer_id = Column(
        Integer,
        ForeignKey(f"{TableName.OFFERS}.id"),
        nullable=False,
    )

    # Understanding version
    version = Column(Integer, nullable=False, default=1)

    # pending | processing | completed | failed
    status = Column(String(20), nullable=False, default="pending")

    # AI-generated knowledge
    product_understanding = Column(Text, nullable=True)
    market_analysis = Column(Text, nullable=True)
    target_audience = Column(JSON, nullable=True)
    pain_points = Column(JSON, nullable=True)
    desires = Column(JSON, nullable=True)
    objections = Column(JSON, nullable=True)
    unique_value = Column(Text, nullable=True)

    # Timestamps
    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
    )

    updated_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
    )