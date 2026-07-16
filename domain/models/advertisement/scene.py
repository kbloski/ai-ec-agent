from sqlalchemy import Column, Integer, String, Text, DateTime
from sqlalchemy.sql import func

from infrastructure.database.db import Base
from common.mixins.json_serializable import JSONSerializable
from domain.enums.table_name import TableName


class Scene(Base, JSONSerializable):

    __tablename__ = TableName.SCENES.value

    # primary key
    id = Column(Integer, primary_key=True, autoincrement=True)

    # scene type
    # examples:
    # problem
    # solution
    # proof
    # product
    # lifestyle
    # cta
    type = Column(String, nullable=False)

    description = Column(Text, nullable=True)

    duration_seconds = Column(Integer, nullable=True)

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
