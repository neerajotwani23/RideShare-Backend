from sqlalchemy import Column, Integer, String, Float, Text, DateTime, Enum as SQLEnum, Numeric
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import enum
from .base import Base

class UserTypeEnum(enum.Enum):
    DRIVER = "driver"
    PASSENGER = "passenger"

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    first_name = Column(String(100), nullable=False)
    last_name = Column(String(100), nullable=False)
    email = Column(String(255), unique=True, index=True, nullable=False)
    password = Column(String(255), nullable=False)
    phone_no = Column(String(20), nullable=True)
    user_type = Column(SQLEnum(UserTypeEnum), nullable=False)
    cnic = Column(String(20), nullable=True)
    profile_picture = Column(String(500), nullable=True)
    bio = Column(Text, nullable=True)
    wallet = Column(Numeric(10, 2), default=0.00)
    driving_license = Column(String(100), nullable=True)
    gender = Column(String(10), nullable=True)
    average_rating = Column(Float, default=0.0)
    created_at = Column(DateTime, default=func.now())
    
    # Relationships
    vehicles = relationship("Vehicle", back_populates="owner", cascade="all, delete-orphan")
    rides_offered = relationship("Ride", back_populates="driver", cascade="all, delete-orphan")
    ride_requests = relationship("RideRequest", back_populates="passenger", cascade="all, delete-orphan")
    transactions = relationship("Transaction", back_populates="user", cascade="all, delete-orphan")
    reviews_given = relationship("RatingsReviews", foreign_keys="RatingsReviews.reviewer_id", back_populates="reviewer", cascade="all, delete-orphan")
    reviews_received = relationship("RatingsReviews", foreign_keys="RatingsReviews.reviewee_id", back_populates="reviewee", cascade="all, delete-orphan")
    payments_sent = relationship("Payment", foreign_keys="Payment.from_user_id", back_populates="sender")
    payments_received = relationship("Payment", foreign_keys="Payment.to_user_id", back_populates="receiver") 