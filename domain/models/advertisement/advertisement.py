from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, JSON
from sqlalchemy.sql import func

from infrastructure.database.db import Base
from common.mixins.json_serializable import JSONSerializable
from domain.enums.table_name import TableName


class Advertisement(Base, JSONSerializable):

    __tablename__ = TableName.ADVERTISEMENTS.value

    # primary key
    id = Column(Integer, primary_key=True, autoincrement=True)

    # relation to product knowledge
    knowledge_id = Column(
        Integer,
        ForeignKey("knowledge.id"),
        nullable=False
    )

    # basic
    name = Column(String, nullable=False)

    # strategy
    strategy_framework = Column(String, nullable=True)
    strategy_angle = Column(String, nullable=True)
    strategy_psychology_trigger = Column(String, nullable=True)
    strategy_awareness_stage = Column(String, nullable=True)
    strategy_hypothesis = Column(Text, nullable=True)

    # creative metadata
    platform = Column(String, nullable=True)
    format = Column(String, nullable=True)
    duration_seconds = Column(Integer, nullable=True)
    aspect_ratio = Column(String, nullable=True)

    # hook
    hook_text = Column(Text, nullable=True)
    hook_type = Column(String, nullable=True)
    hook_visual = Column(Text, nullable=True)
    hook_duration = Column(Integer, nullable=True)

    # main message
    problem = Column(Text, nullable=True)
    solution = Column(Text, nullable=True)

    # proof
    proof_type = Column(String, nullable=True)
    proof_content = Column(Text, nullable=True)

    # voice
    voiceover = Column(Text, nullable=True)

    # audience
    audience_description = Column(Text, nullable=True)

    # cta
    cta_text = Column(String, nullable=True)
    cta_type = Column(String, nullable=True)
    cta_urgency = Column(String, nullable=True)

    # json fields
    visual_direction = Column(JSON, nullable=True)
    text_overlays = Column(JSON, nullable=True)

    # score
    score_hook = Column(Integer, nullable=True)
    score_emotion = Column(Integer, nullable=True)
    score_clarity = Column(Integer, nullable=True)
    score_purchase_intent = Column(Integer, nullable=True)
    score_overall = Column(Integer, nullable=True)

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
