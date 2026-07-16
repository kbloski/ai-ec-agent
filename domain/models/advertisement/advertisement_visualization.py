from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.sql import func

from infrastructure.database.db import Base
from common.mixins.json_serializable import JSONSerializable
from domain.enums.table_name import TableName


class AdvertisementVisualization(Base, JSONSerializable):

    __tablename__ = TableName.ADVERTISEMENT_VISUALIZATIONS.value

    # primary key
    id = Column(Integer, primary_key=True, autoincrement=True)

    advertisement_id = Column(
        Integer,
        ForeignKey("advertisements.id"),
        nullable=False
    )

    scene_id = Column(
        Integer,
        ForeignKey("scenes.id"),
        nullable=True
    )

    # display order
    order_number = Column(Integer, nullable=False, default=1)

    type = Column(String, nullable=True)

    description = Column(Text, nullable=True)

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now()
    )
