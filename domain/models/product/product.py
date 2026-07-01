from sqlalchemy import Column, Integer, String, Numeric, JSON, DateTime
from datetime import datetime
from infrastructure.database.db import Base

class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    buying_price = Column(Numeric, nullable=True)

    raw_description = Column(String, nullable=True)
    raw_problems = Column(JSON, nullable=True)
    raw_audience = Column(JSON, nullable=True)

    # created_at = Column(DateTime, default=datetime.utcnow)