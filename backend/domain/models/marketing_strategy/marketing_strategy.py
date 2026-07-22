from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, JSON
from sqlalchemy.sql import func

from infrastructure.database.db import Base
from common.mixins.json_serializable import JSONSerializable
from domain.enums.table_name import TableName


class MarketingStrategy(Base, JSONSerializable):

    __tablename__ = TableName.MARKETING_STRATEGY.value

    # primary key
    id = Column(Integer, primary_key=True, autoincrement=True)

    # relations
    brand_marketing_id = Column(
        Integer,
        ForeignKey(TableName.BRAND_MARKETING + ".id", ondelete="CASCADE"),
        nullable=False
    )

    marketing_objective = Column(Text, nullable=True)
    growth_strategy = Column(Text, nullable=True)

    primary_audience = Column(JSON, nullable=True)
    secondary_audience = Column(JSON, nullable=True)
    audience_prioritization = Column(JSON, nullable=True)

    customer_journey = Column(JSON, nullable=True)

    marketing_channels = Column(JSON, nullable=True)

    acquisition_strategy = Column(JSON, nullable=True)
    trust_building_strategy = Column(JSON, nullable=True)

    content_strategy = Column(JSON, nullable=True)

    community_strategy = Column(JSON, nullable=True)
    creator_influencer_strategy = Column(JSON, nullable=True)

    campaign_directions = Column(JSON, nullable=True)

    conversion_strategy = Column(JSON, nullable=True)
    retention_strategy = Column(JSON, nullable=True)

    marketing_experiments = Column(JSON, nullable=True)
    marketing_kpis = Column(JSON, nullable=True)

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
