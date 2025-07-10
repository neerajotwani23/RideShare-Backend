from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, Enum as SQLEnum
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import enum
from .base import Base
from .ride import GenderPreferenceEnum

class RideRequestStatusEnum(enum.Enum):
    PENDING = "pending"
    ACCEPTED = "accepted"
    REJECTED = "rejected"
    CANCELLED = "cancelled"

class RideRequest(Base):
    __tablename__ = "ride_requests"
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)  # Passenger
    ride_id = Column(Integer, ForeignKey("rides.id"), nullable=False)
    datetime = Column(DateTime, default=func.now())
    status = Column(SQLEnum(RideRequestStatusEnum), nullable=False, default=RideRequestStatusEnum.PENDING)
    seats = Column(Integer, nullable=False)
    # Optional fields for custom requests
    source = Column(String(255), nullable=True)
    destination = Column(String(255), nullable=True)
    ac = Column(Boolean, default=False)
    smoking = Column(Boolean, default=False)
    music = Column(Boolean, default=False)
    gender_preference = Column(SQLEnum(GenderPreferenceEnum), default=GenderPreferenceEnum.ANY)
    
    # Relationships
    passenger = relationship("User", back_populates="ride_requests")
    ride = relationship("Ride", back_populates="ride_requests") 