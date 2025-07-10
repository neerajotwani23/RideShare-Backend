from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from .base import Base

class Vehicle(Base):
    __tablename__ = "vehicles"
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    model = Column(String(100), nullable=True)
    name_make = Column(String(100), nullable=True)  # Brand/Make
    color = Column(String(50), nullable=True)
    no_plate = Column(String(20), nullable=True)
    registration = Column(String(100), nullable=True)
    created_at = Column(DateTime, default=func.now())
    
    # Relationships
    owner = relationship("User", back_populates="vehicles") 