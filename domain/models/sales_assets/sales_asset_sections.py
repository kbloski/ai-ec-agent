from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.sql import func

from infrastructure.database.db import Base
from common.mixins.json_serializable import JSONSerializable
from domain.enums.table_name import TableName


class SalesAssetSection(Base, JSONSerializable):

    __tablename__ = TableName.SALES_ASSET_SECTIONS.value

    # primary key
    id = Column(
        Integer,
        primary_key=True,
        autoincrement=True
    )

    # parent sales asset
    sales_asset_id = Column(
        Integer,
        ForeignKey("sales_assets.id"),
        nullable=False
    )

    # section type
    type = Column(
        String,
        nullable=False
    )

    # display order
    position = Column(
        Integer,
        nullable=False,
        default=1
    )

    # internal section name
    name = Column(
        String,
        nullable=False
    )

    # sales purpose of this section
    goal = Column(
        Text,
        nullable=True
    )

    # main headline
    headline = Column(
        String,
        nullable=True
    )

    # supporting headline
    subheadline = Column(
        Text,
        nullable=True
    )

    # main section content
    content = Column(
        Text,
        nullable=True
    )

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