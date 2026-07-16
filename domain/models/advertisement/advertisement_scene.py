from sqlalchemy import Column, Integer, DateTime, ForeignKey
from sqlalchemy.sql import func

from infrastructure.database.db import Base
from common.mixins.json_serializable import JSONSerializable
from domain.enums.table_name import TableName


class AdvertisementScene(Base, JSONSerializable):

    __tablename__ = TableName.ADVERTISEMENT_SCENES.value

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
        nullable=False
    )

    # display order
    order_number = Column(Integer, nullable=False, default=1)

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now()
    )
