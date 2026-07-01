from sqlalchemy import Column, Integer, String, Numeric, JSON, DateTime
from sqlalchemy.sql import func
from infrastructure.database.db import Base


class Product(Base):
    __tablename__ = "products"

    # primary key auto-increment
    id = Column(Integer, primary_key=True, autoincrement=True)

    # basic info
    name = Column(String, nullable=False)

    # pricing
    buying_price = Column(Numeric(10, 2), nullable=True)  # REQUIRED
    selling_price = Column(Numeric(10, 2), nullable=False)  # OPTIONAL

    # (user-provided fact)
    description = Column(String, nullable=True)

    # (user-provided fact)
    target_audience = Column(JSON, nullable=True)  # list[str]
    pain_points = Column(JSON, nullable=True)      # list[str]

    # timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())