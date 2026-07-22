from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, JSON
from sqlalchemy.sql import func

from infrastructure.database.db import Base
from common.mixins.json_serializable import JSONSerializable
from domain.enums.table_name import TableName


class VideoCreativeExecution(Base, JSONSerializable):

    __tablename__ = TableName.VIDEO_CREATIVE_EXECUTION.value

    # primary key
    id = Column(Integer, primary_key=True, autoincrement=True)

    # relations
    ad_execution_id = Column(
        Integer,
        ForeignKey(TableName.AD_EXECUTION + ".id", ondelete="CASCADE"),
        nullable=False
    )

    duration_seconds = Column(Integer, nullable=True)

    hook_strategy = Column(JSON, nullable=True)
    structure = Column(JSON, nullable=True)
    scenes = Column(JSON, nullable=True)
    asset_requirements = Column(JSON, nullable=True)
    production_notes = Column(JSON, nullable=True)
    cta = Column(JSON, nullable=True)

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
