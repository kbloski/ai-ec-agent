from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, JSON
from sqlalchemy.sql import func

from infrastructure.database.db import Base
from common.mixins.json_serializable import JSONSerializable
from domain.enums.table_name import TableName


class CreativeStrategy(Base, JSONSerializable):

    __tablename__ = TableName.CREATIVE_STRATEGY.value

    # primary key
    id = Column(Integer, primary_key=True, autoincrement=True)

    # relations
    ad_strategy_id = Column(
        Integer,
        ForeignKey(TableName.AD_STRATEGY + ".id", ondelete="CASCADE"),
        nullable=False
    )

    name = Column(String, nullable=True)
    objective = Column(String, nullable=True)
    creative_type = Column(String, nullable=True)
    recommended_format = Column(String, nullable=True)

    target = Column(JSON, nullable=True)
    creative_big_idea = Column(String, nullable=True)
    message_angle = Column(String, nullable=True)
    hook_strategy = Column(JSON, nullable=True)
    story_framework = Column(JSON, nullable=True)
    creative_direction = Column(JSON, nullable=True)
    speaker_strategy = Column(JSON, nullable=True)
    emotion_flow = Column(JSON, nullable=True)
    proof_strategy = Column(JSON, nullable=True)
    execution_guidelines = Column(JSON, nullable=True)

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
