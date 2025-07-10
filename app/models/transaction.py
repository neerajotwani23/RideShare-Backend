import enum
from sqlalchemy import Column, Integer, DateTime, ForeignKey, Enum as SQLEnum, Numeric
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from .base import Base

class TransactionTypeEnum(enum.Enum):
    DEBIT = "debit"
    CREDIT = "credit"

class Transaction(Base):
    __tablename__ = "transactions"
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    ride_id = Column(Integer, ForeignKey("rides.id"), nullable=True)
    type = Column(SQLEnum(TransactionTypeEnum), nullable=False)
    datetime = Column(DateTime, default=func.now())
    amount = Column(Numeric(10, 2), nullable=False)
    
    # Relationships
    user = relationship("User", back_populates="transactions")
    ride = relationship("Ride", back_populates="transactions")
    payment = relationship("Payment", back_populates="transaction", uselist=False) 