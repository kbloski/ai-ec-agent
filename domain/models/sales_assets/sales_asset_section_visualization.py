from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.sql import func

from infrastructure.database.db import Base
from common.mixins.json_serializable import JSONSerializable
from domain.enums.table_name import TableName


class SalesAssetSectionVisualization(Base, JSONSerializable):

    __tablename__ = TableName.SALES_ASSET_SECTION_VISUALIZATIONS.value

    sales_asset_section_id = Column(
        Integer,
        ForeignKey("sales_asset_sections.id"),
        nullable=False,
        primary_key=True
    )


    visualization_id = Column(
        Integer,
        ForeignKey("visualizations.id"),
        nullable=False,
        primary_key=True
    )


    position = Column(
        Integer,
        nullable=False,
        default=1
    )


    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now()
    )