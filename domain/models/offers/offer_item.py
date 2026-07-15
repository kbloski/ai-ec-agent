from sqlalchemy import Column, Integer, String, Numeric, JSON, DateTime, ForeignKey
from sqlalchemy.sql import func
from common.mixins.json_serializable import JSONSerializable
from infrastructure.database.db import Base
from domain.enums.table_name import TableName


class OfferItem(Base, JSONSerializable):
    __tablename__ = TableName.OFFER_ITEMS.value

    id = Column(Integer, primary_key=True, autoincrement=True)

    offer_id = Column(
        Integer,
        ForeignKey(TableName.OFFERS + ".id", ondelete="CASCADE"),
        nullable=False
    )

    name = Column(String, nullable=False)
    quantity = Column(Integer, nullable=False, default=1)
    details = Column(String, nullable=True)

    # timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())