import enum
from sqlalchemy import Column, Integer, ForeignKey, Enum as SQLEnum, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from .base import Base

class PaymentTypeEnum(enum.Enum):
    CASH = "cash"
    WALLET = "wallet"

class Payment(Base):
    __tablename__ = "payments"
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    type = Column(SQLEnum(PaymentTypeEnum), nullable=False)
    transaction_id = Column(Integer, ForeignKey("transactions.id"), nullable=False, unique=True)
    from_user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    to_user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    created_at = Column(DateTime, default=func.now())
    
    # Relationships
    transaction = relationship("Transaction", back_populates="payment")
    sender = relationship("User", foreign_keys=[from_user_id], back_populates="payments_sent")
    receiver = relationship("User", foreign_keys=[to_user_id], back_populates="payments_received") 