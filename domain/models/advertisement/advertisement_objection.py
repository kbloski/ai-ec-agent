from sqlalchemy import Column, Integer, Text, DateTime, ForeignKey
from sqlalchemy.sql import func

from infrastructure.database.db import Base
from common.mixins.json_serializable import JSONSerializable
from domain.enums.table_name import TableName


class AdvertisementObjection(Base, JSONSerializable):

    __tablename__ = TableName.ADVERTISEMENT_OBJECTIONS.value

    # primary key
    id = Column(Integer, primary_key=True, autoincrement=True)

    advertisement_id = Column(
        Integer,
        ForeignKey("advertisements.id"),
        nullable=False
    )

    objection = Column(Text, nullable=False)

    answer = Column(Text, nullable=True)

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now()
    )
