from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.sql import func

from infrastructure.database.db import Base
from common.mixins.json_serializable import JSONSerializable
from domain.enums.table_name import TableName

class Visualization(Base, JSONSerializable):

    __tablename__ = TableName.VISUALIZATIONS.value


    id = Column(
        Integer,
        primary_key=True,
        autoincrement=True
    )


    # image, video, infographic...
    format = Column(
        String,
        nullable=False
    )


    # internal name
    name = Column(
        String,
        nullable=False
    )


    # what this visualization represents
    description = Column(
        Text,
        nullable=False
    )


    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now()
    )


    updated_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now()
    )