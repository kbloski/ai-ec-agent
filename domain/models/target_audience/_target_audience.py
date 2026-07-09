from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Float, Index
from sqlalchemy.sql import func

from infrastructure.database.db import Base
from common.mixins.json_serializable import JSONSerializable
from domain.enums.table_name import TableName


class TargetAudience(Base, JSONSerializable):
    __tablename__ = TableName.TARGET_AUDIENCES

    # Primary key
    id = Column(Integer, primary_key=True, autoincrement=True)

    # Relation to offer
    # offer_id = Column(
    #     Integer,
    #     ForeignKey(TableName.OFFERS + ".id"),
    #     nullable=False,
    #     index=True,
    # )

    # Optional relation to knowledge/AI analysis
    knowledge_id = Column(
        Integer,
        ForeignKey(TableName.OFFER_KNOWLEDGE + ".id"),
        nullable=True,
        index=True,
    )

    # Basic information
    name = Column(String(255),nullable=False )
    reason = Column( String, nullable=True)

    # AI evaluation
    score = Column(  Float, nullable=True,)

    confidence = Column( Float,  nullable=True,)

    # Demographics
    age_min = Column( Integer,  nullable=True)
    age_max = Column( Integer, nullable=True )

    gender = Column( String(50), nullable=True )

    location = Column( String(255),nullable=True,)

    # budget
    # mass_market
    # middle
    # affluent
    # premium
    # luxury
    income_level = Column( String(50),  nullable=True ) #poziom dochodów


    # Buying psychology
    # 1. unaware
    # 2. problem_aware
    # 3. solution_aware
    # 4. product_aware
    # 5. most_aware
    awareness_level = Column(  String(50), nullable=True ) #swiadomość klienta

    price_sensitivity = Column(  String(50),  nullable=True )

    research_level = Column(  String(50), nullable=True )

    decision_time = Column(  String(50), nullable=True )


    # Status
    content_status = Column(
        String(20),
        nullable=False,
        index=True,
    )


    # timestamps
    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
    )

    updated_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
    )


    __table_args__ = (
        Index(
            "ix_target_audience_offer_status",
            "offer_id",
            "content_status"
        ),
        Index(
            "ix_target_audience_offer_score",
            "offer_id",
            "score"
        ),
    )