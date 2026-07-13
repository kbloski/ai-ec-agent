from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, JSON
from sqlalchemy.sql import func

from infrastructure.database.db import Base
from common.mixins.json_serializable import JSONSerializable
from domain.enums.table_name import TableName


class OfferKnowledge(Base, JSONSerializable):
    __tablename__ = TableName.OFFER_KNOWLEDGE

    # Primary key
    id = Column(Integer, primary_key=True, autoincrement=True)

    # Related offer
    offer_id = Column(
        Integer,
        ForeignKey(TableName.OFFERS+".id"),
        nullable=False,
    )

    # Understanding version
    version = Column(Integer, nullable=False, default=1)

    # pending | processing | completed | failed
    content_status = Column(String(20), nullable=False)

    # AI-generated knowledge
    offer_summary = Column(Text, nullable=True)
    category = Column(Text, nullable=True)

    value_proposition=Column(Text, nullable=True)

    #TODO - prompt 
    #TODO - object used to prompt 

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