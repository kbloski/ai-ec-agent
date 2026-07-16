from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.sql import func

from infrastructure.database.db import Base
from common.mixins.json_serializable import JSONSerializable
from domain.enums.table_name import TableName


class Experiment(Base, JSONSerializable):

    __tablename__ = TableName.KNOWLEDGE_EXPERIMENTS.value

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
    description = Column(Text, nullable=True)

    # classification
    experiment_type = Column(String, nullable=True)
    framework = Column(String, nullable=True)
    angle = Column(String, nullable=True)
    psychology_trigger = Column(String, nullable=True)
    awareness_stage = Column(String, nullable=True)

    # hypothesis
    hypothesis = Column(Text, nullable=True)
    expected_result = Column(Text, nullable=True)

    # customer insight
    primary_problem = Column(Text, nullable=True)
    primary_desire = Column(Text, nullable=True)
    primary_fear = Column(Text, nullable=True)
    dream_outcome = Column(Text, nullable=True)

    # big idea
    big_idea = Column(Text, nullable=True)
    big_promise = Column(Text, nullable=True)
    unique_mechanism = Column(Text, nullable=True)
    core_message = Column(Text, nullable=True)

    # strategy
    offer_strategy = Column(Text, nullable=True)
    urgency_strategy = Column(Text, nullable=True)
    cta_strategy = Column(Text, nullable=True)
    proof_strategy = Column(Text, nullable=True)

    # scoring
    priority = Column(Integer, nullable=True)
    confidence = Column(Integer, nullable=True)

    # state
    status = Column(String, nullable=False, default="DRAFT")
    notes = Column(Text, nullable=True)

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
