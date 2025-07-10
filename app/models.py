from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime, Text, ForeignKey, Enum as SQLEnum
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from .database import Base
import enum

# Enums for type-safe choices
class TransactionTypeEnum(enum.Enum):
    DEBIT = "debit"
    CREDIT = "credit"

class PaymentTypeEnum(enum.Enum):
    CASH = "cash"
    WALLET = "wallet"

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    first_name = Column(String(100), nullable=False)
    last_name = Column(String(100), nullable=False)
    email = Column(String(255), unique=True, index=True, nullable=False)
    password = Column(String(255), nullable=False)
    phone_no = Column(String(20), nullable=True)
    user_type = Column(String(50), nullable=True)  # e.g., 'driver', 'passenger', 'both'
    cnic = Column(String(20), nullable=True)
    profile_picture = Column(String(500), nullable=True)
    bio = Column(Text, nullable=True)
    wallet = Column(Float, default=0.0)
    driving_license = Column(String(100), nullable=True)
    gender = Column(String(10), nullable=True)
    average_rating = Column(Float, default=0.0)
    
    # Relationships
    vehicles = relationship("Vehicle", back_populates="owner", cascade="all, delete-orphan")
    rides_offered = relationship("Ride", back_populates="driver", cascade="all, delete-orphan")
    ride_requests = relationship("RideRequest", back_populates="passenger", cascade="all, delete-orphan")
    transactions = relationship("Transaction", back_populates="user", cascade="all, delete-orphan")
    ratings_given = relationship("RatingsReviews", back_populates="reviewer", cascade="all, delete-orphan")
    payments_sent = relationship("Payment", foreign_keys="Payment.from_user_id", back_populates="sender")
    payments_received = relationship("Payment", foreign_keys="Payment.to_user_id", back_populates="receiver")

class Vehicle(Base):
    __tablename__ = "vehicles"
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    model = Column(String(100), nullable=False)
    name_make = Column(String(100), nullable=False)  # Brand/Make
    color = Column(String(50), nullable=True)
    no_plate = Column(String(20), unique=True, nullable=False)
    registration = Column(String(100), nullable=True)
    
    # Relationships
    owner = relationship("User", back_populates="vehicles")

class Ride(Base):
    __tablename__ = "rides"
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)  # Driver
    timing = Column(DateTime, nullable=False)
    status = Column(String(50), default="active")  # active, completed, cancelled
    source = Column(String(255), nullable=False)
    destination = Column(String(255), nullable=False)
    fare = Column(Float, nullable=False)
    seats_offered = Column(Integer, nullable=False)
    ac = Column(Boolean, default=False)
    smoking = Column(Boolean, default=False)
    music = Column(Boolean, default=False)
    gender_preference = Column(Boolean, default=False)
    
    # Relationships
    driver = relationship("User", back_populates="rides_offered")
    ride_requests = relationship("RideRequest", back_populates="ride", cascade="all, delete-orphan")
    transactions = relationship("Transaction", back_populates="ride", cascade="all, delete-orphan")
    ratings = relationship("RatingsReviews", back_populates="ride", cascade="all, delete-orphan")

class RideRequest(Base):
    __tablename__ = "ride_requests"
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)  # Passenger
    ride_id = Column(Integer, ForeignKey("rides.id"), nullable=False)
    datetime = Column(DateTime, default=func.now())
    status = Column(String(50), default="pending")  # pending, accepted, rejected, completed
    source = Column(String(255), nullable=False)
    destination = Column(String(255), nullable=False)
    seats = Column(Integer, nullable=False)
    ac = Column(Boolean, default=False)
    smoking = Column(Boolean, default=False)
    music = Column(Boolean, default=False)
    gender_preference = Column(Boolean, default=False)
    
    # Relationships
    passenger = relationship("User", back_populates="ride_requests")
    ride = relationship("Ride", back_populates="ride_requests")

class Transaction(Base):
    __tablename__ = "transactions"
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    ride_id = Column(Integer, ForeignKey("rides.id"), nullable=True)
    type = Column(SQLEnum(TransactionTypeEnum), nullable=False)
    datetime = Column(DateTime, default=func.now())
    amount = Column(Float, nullable=False)
    
    # Relationships
    user = relationship("User", back_populates="transactions")
    ride = relationship("Ride", back_populates="transactions")
    payment = relationship("Payment", back_populates="transaction", uselist=False)

class RatingsReviews(Base):
    __tablename__ = "ratings_reviews"
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)  # Reviewer
    ride_id = Column(Integer, ForeignKey("rides.id"), nullable=False)
    stars = Column(Integer, nullable=False)  # 1-5 rating
    text_review = Column(Text, nullable=True)
    
    # Relationships
    reviewer = relationship("User", back_populates="ratings_given")
    ride = relationship("Ride", back_populates="ratings")

class Payment(Base):
    __tablename__ = "payments"
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    type = Column(SQLEnum(PaymentTypeEnum), nullable=False)
    transaction_id = Column(Integer, ForeignKey("transactions.id"), nullable=False)
    from_user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    to_user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    
    # Relationships
    transaction = relationship("Transaction", back_populates="payment")
    sender = relationship("User", foreign_keys=[from_user_id], back_populates="payments_sent")
    receiver = relationship("User", foreign_keys=[to_user_id], back_populates="payments_received")
