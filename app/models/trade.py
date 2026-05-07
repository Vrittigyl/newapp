from sqlalchemy import Column, Integer, String, Float
from app.database import Base


class Trade(Base):
    __tablename__ = "trades"

    id = Column(Integer, primary_key=True, index=True)

    symbol = Column(String, nullable=False)

    trade_type = Column(String, nullable=False)

    quantity = Column(Integer, nullable=False)

    price = Column(Float, nullable=False)

    timestamp = Column(String, nullable=False)