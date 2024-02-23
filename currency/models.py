from datetime import datetime

from sqlalchemy import Column, Integer, String, Float, DateTime

from db import Base


class Currency(Base):
    __tablename__ = "currency"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True)
    code = Column(Integer, unique=True, nullable=True)
    rate = Column(Float)
    timestamp = Column(DateTime, default=datetime.utcnow)
