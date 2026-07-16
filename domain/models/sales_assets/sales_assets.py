from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.sql import func

from infrastructure.database.db import Base
from common.mixins.json_serializable import JSONSerializable
from domain.enums.table_name import TableName


class SalesAsset(Base, JSONSerializable):
    __tablename__ = TableName.SALES_ASSETS.value


    # primary key auto-increment
    id = Column(Integer, primary_key=True, autoincrement=True)


    # relation to product knowledge
    knowledge_id = Column(
        Integer,
        ForeignKey("knowledge.id"),
        nullable=False
    )


    # type of sales asset
    # examples:
    # landing_page
    # advertorial
    # vsl
    # email
    type = Column(
        String,
        nullable=False
    )

    # internal name
    name = Column(
        String,
        nullable=False
    )

    # main marketing angle
    # example:
    # "Maintain your garden without physical strain"
    main_angle = Column(
        String,
        nullable=True
    )

    content_status = Column(
        String,
        nullable=False,
        default="draft"
    )


    # asset iteration
    version = Column(
        Integer,
        nullable=False,
        default=1
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