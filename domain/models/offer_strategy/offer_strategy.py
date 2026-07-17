from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, JSON
from sqlalchemy.sql import func

from infrastructure.database.db import Base
from common.mixins.json_serializable import JSONSerializable
from domain.enums.table_name import TableName


class OfferStrategy(Base, JSONSerializable):

    __tablename__ = TableName.OFFER_STRATEGY.value

    # primary key
    id = Column(Integer, primary_key=True, autoincrement=True)

    # relations
    knowledge_id = Column(
        Integer,
        ForeignKey("knowledge.id"),
        nullable=False
    )

    brand_marketing_id = Column(
        Integer,
        ForeignKey(TableName.BRAND_MARKETING + ".id"),
        nullable=False
    )

    marketing_strategy_id = Column(
        Integer,
        ForeignKey(TableName.MARKETING_STRATEGY + ".id"),
        nullable=False
    )

    offer_name = Column(String, nullable=True)
    offer_positioning = Column(Text, nullable=True)

    core_value_proposition = Column(Text, nullable=True)
    main_customer_problem = Column(Text, nullable=True)
    solution_mechanism = Column(Text, nullable=True)

    primary_benefit = Column(Text, nullable=True)
    secondary_benefits = Column(JSON, nullable=True)
    functional_benefits = Column(JSON, nullable=True)
    emotional_benefits = Column(JSON, nullable=True)

    offer_structure = Column(JSON, nullable=True)
    value_stack = Column(JSON, nullable=True)

    risk_reversal = Column(JSON, nullable=True)
    trust_elements = Column(JSON, nullable=True)

    pricing_strategy = Column(Text, nullable=True)
    urgency_strategy = Column(Text, nullable=True)

    customer_objection_handling = Column(JSON, nullable=True)
    competitive_difference = Column(Text, nullable=True)

    conversion_levers = Column(JSON, nullable=True)

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
