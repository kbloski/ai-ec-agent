from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, JSON
from sqlalchemy.sql import func

from infrastructure.database.db import Base
from common.mixins.json_serializable import JSONSerializable
from domain.enums.table_name import TableName


class Experiment(Base, JSONSerializable):

    __tablename__ = TableName.EXPERIMENTS.value

    # primary key
    id = Column(Integer, primary_key=True, autoincrement=True)

    # parent experiment strategy
    experiment_strategy_id = Column(
        Integer,
        ForeignKey(TableName.EXPERIMENT_STRATEGY + ".id"),
        nullable=False
    )

    name = Column(String, nullable=True)
    category = Column(String, nullable=True)

    strategic_question = Column(Text, nullable=True)
    objective = Column(Text, nullable=True)

    hypothesis = Column(Text, nullable=True)
    hypothesis_basis = Column(JSON, nullable=True)
    reason = Column(Text, nullable=True)

    target_audience = Column(Text, nullable=True)
    funnel_stage = Column(String, nullable=True)
    channel = Column(String, nullable=True)
    asset_type = Column(String, nullable=True)

    variable_tested = Column(Text, nullable=True)
    control_variant = Column(Text, nullable=True)
    test_variant = Column(Text, nullable=True)

    success_metrics = Column(JSON, nullable=True)
    decision_rule = Column(Text, nullable=True)
    expected_learning = Column(Text, nullable=True)

    priority = Column(JSON, nullable=True)

    estimated_cost = Column(String, nullable=True)
    estimated_duration = Column(String, nullable=True)

    status = Column(String, nullable=False, default="planned")

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
