from sqlalchemy.orm import Session
from sqlalchemy import and_, or_, func
from datetime import datetime, date
from typing import Optional, List
from . import models, schemas
from fastapi import HTTPException, status
from passlib.context import CryptContext

# Password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

# ============== USER CRUD ==============
def create_user(db: Session, user: schemas.UserCreate):
    # Check if email already exists
    db_user = db.query(models.User).filter(models.User.email == user.email).first()
    if db_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    
    # Hash password and create user
    hashed_password = get_password_hash(user.password)
    user_data = user.dict()
    user_data["password"] = hashed_password
    
    db_user = models.User(**user_data)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def authenticate_user(db: Session, email: str, password: str):
    user = db.query(models.User).filter(models.User.email == email).first()
    if not user or not verify_password(password, user.password):
        return None
    return user

def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()

def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()

def update_user(db: Session, user_id: int, user_update: schemas.UserUpdate):
    db_user = get_user(db, user_id)
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    
    update_data = user_update.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_user, field, value)
    
    db.commit()
    db.refresh(db_user)
    return db_user

def update_user_wallet(db: Session, user_id: int, amount: float):
    db_user = get_user(db, user_id)
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    
    db_user.wallet += amount
    db.commit()
    db.refresh(db_user)
    return db_user

def update_user_rating(db: Session, user_id: int):
    """Recalculate and update user's average rating"""
    avg_rating = db.query(func.avg(models.RatingsReviews.stars)).filter(
        models.RatingsReviews.user_id == user_id
    ).scalar()
    
    db_user = get_user(db, user_id)
    if db_user:
        db_user.average_rating = float(avg_rating) if avg_rating else 0.0
        db.commit()
        db.refresh(db_user)
    return db_user

# ============== VEHICLE CRUD ==============
def create_vehicle(db: Session, vehicle: schemas.VehicleCreate):
    # Check if plate number already exists
    existing_vehicle = db.query(models.Vehicle).filter(
        models.Vehicle.no_plate == vehicle.no_plate
    ).first()
    if existing_vehicle:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Vehicle with this plate number already exists"
        )
    
    db_vehicle = models.Vehicle(**vehicle.dict())
    db.add(db_vehicle)
    db.commit()
    db.refresh(db_vehicle)
    return db_vehicle

def get_vehicles_by_user(db: Session, user_id: int):
    return db.query(models.Vehicle).filter(models.Vehicle.user_id == user_id).all()

def get_vehicle(db: Session, vehicle_id: int):
    return db.query(models.Vehicle).filter(models.Vehicle.id == vehicle_id).first()

def update_vehicle(db: Session, vehicle_id: int, vehicle_update: schemas.VehicleUpdate):
    db_vehicle = get_vehicle(db, vehicle_id)
    if not db_vehicle:
        raise HTTPException(status_code=404, detail="Vehicle not found")
    
    update_data = vehicle_update.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_vehicle, field, value)
    
    db.commit()
    db.refresh(db_vehicle)
    return db_vehicle

def delete_vehicle(db: Session, vehicle_id: int):
    db_vehicle = get_vehicle(db, vehicle_id)
    if not db_vehicle:
        raise HTTPException(status_code=404, detail="Vehicle not found")
    
    db.delete(db_vehicle)
    db.commit()
    return {"message": "Vehicle deleted successfully"}

# ============== RIDE CRUD ==============
def create_ride(db: Session, ride: schemas.RideCreate):
    db_ride = models.Ride(**ride.dict())
    db.add(db_ride)
    db.commit()
    db.refresh(db_ride)
    return db_ride

def get_ride(db: Session, ride_id: int):
    return db.query(models.Ride).filter(models.Ride.id == ride_id).first()

def get_rides_by_user(db: Session, user_id: int):
    return db.query(models.Ride).filter(models.Ride.user_id == user_id).all()

def search_rides(db: Session, search_params: schemas.RideSearchParams, skip: int = 0, limit: int = 10):
    query = db.query(models.Ride).filter(models.Ride.status == "active")
    
    if search_params.source:
        query = query.filter(models.Ride.source.ilike(f"%{search_params.source}%"))
    if search_params.destination:
        query = query.filter(models.Ride.destination.ilike(f"%{search_params.destination}%"))
    if search_params.date:
        search_date = datetime.strptime(search_params.date, "%Y-%m-%d").date()
        query = query.filter(func.date(models.Ride.timing) == search_date)
    if search_params.min_seats:
        query = query.filter(models.Ride.seats_offered >= search_params.min_seats)
    if search_params.max_fare:
        query = query.filter(models.Ride.fare <= search_params.max_fare)
    if search_params.ac is not None:
        query = query.filter(models.Ride.ac == search_params.ac)
    if search_params.smoking is not None:
        query = query.filter(models.Ride.smoking == search_params.smoking)
    if search_params.music is not None:
        query = query.filter(models.Ride.music == search_params.music)
    if search_params.gender_preference is not None:
        query = query.filter(models.Ride.gender_preference == search_params.gender_preference)
    
    return query.offset(skip).limit(limit).all()

def update_ride(db: Session, ride_id: int, ride_update: schemas.RideUpdate):
    db_ride = get_ride(db, ride_id)
    if not db_ride:
        raise HTTPException(status_code=404, detail="Ride not found")
    
    update_data = ride_update.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_ride, field, value)
    
    db.commit()
    db.refresh(db_ride)
    return db_ride

def cancel_ride(db: Session, ride_id: int):
    db_ride = get_ride(db, ride_id)
    if not db_ride:
        raise HTTPException(status_code=404, detail="Ride not found")
    
    db_ride.status = "cancelled"
    db.commit()
    db.refresh(db_ride)
    return db_ride

# ============== RIDE REQUEST CRUD ==============
def create_ride_request(db: Session, ride_request: schemas.RideRequestCreate):
    # Check if ride exists and is active
    ride = get_ride(db, ride_request.ride_id)
    if not ride or ride.status != "active":
        raise HTTPException(status_code=404, detail="Ride not found or not active")
    
    # Check if user already has a pending request for this ride
    existing_request = db.query(models.RideRequest).filter(
        and_(
            models.RideRequest.user_id == ride_request.user_id,
            models.RideRequest.ride_id == ride_request.ride_id,
            models.RideRequest.status == "pending"
        )
    ).first()
    
    if existing_request:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="You already have a pending request for this ride"
        )
    
    db_request = models.RideRequest(**ride_request.dict())
    db.add(db_request)
    db.commit()
    db.refresh(db_request)
    return db_request

def get_ride_request(db: Session, request_id: int):
    return db.query(models.RideRequest).filter(models.RideRequest.id == request_id).first()

def get_ride_requests_by_user(db: Session, user_id: int):
    return db.query(models.RideRequest).filter(models.RideRequest.user_id == user_id).all()

def get_ride_requests_for_ride(db: Session, ride_id: int):
    return db.query(models.RideRequest).filter(models.RideRequest.ride_id == ride_id).all()

def update_ride_request_status(db: Session, request_id: int, status: str):
    db_request = get_ride_request(db, request_id)
    if not db_request:
        raise HTTPException(status_code=404, detail="Ride request not found")
    
    db_request.status = status
    db.commit()
    db.refresh(db_request)
    return db_request

# ============== TRANSACTION CRUD ==============
def create_transaction(db: Session, transaction: schemas.TransactionCreate):
    db_transaction = models.Transaction(**transaction.dict())
    db.add(db_transaction)
    db.commit()
    db.refresh(db_transaction)
    
    # Update user wallet
    if transaction.type == schemas.TransactionType.CREDIT:
        update_user_wallet(db, transaction.user_id, transaction.amount)
    else:  # DEBIT
        update_user_wallet(db, transaction.user_id, -transaction.amount)
    
    return db_transaction

def get_transactions_by_user(db: Session, user_id: int, skip: int = 0, limit: int = 10):
    return db.query(models.Transaction).filter(
        models.Transaction.user_id == user_id
    ).order_by(models.Transaction.datetime.desc()).offset(skip).limit(limit).all()

# ============== RATINGS & REVIEWS CRUD ==============
def create_rating(db: Session, rating: schemas.RatingCreate):
    # Check if user already rated this ride
    existing_rating = db.query(models.RatingsReviews).filter(
        and_(
            models.RatingsReviews.user_id == rating.user_id,
            models.RatingsReviews.ride_id == rating.ride_id
        )
    ).first()
    
    if existing_rating:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="You have already rated this ride"
        )
    
    db_rating = models.RatingsReviews(**rating.dict())
    db.add(db_rating)
    db.commit()
    db.refresh(db_rating)
    
    # Update driver's average rating
    ride = get_ride(db, rating.ride_id)
    if ride:
        update_user_rating(db, ride.user_id)
    
    return db_rating

def get_ratings_for_ride(db: Session, ride_id: int):
    return db.query(models.RatingsReviews).filter(models.RatingsReviews.ride_id == ride_id).all()

def get_ratings_by_user(db: Session, user_id: int):
    return db.query(models.RatingsReviews).filter(models.RatingsReviews.user_id == user_id).all()

# ============== PAYMENT CRUD ==============
def create_payment(db: Session, payment: schemas.PaymentCreate):
    db_payment = models.Payment(**payment.dict())
    db.add(db_payment)
    db.commit()
    db.refresh(db_payment)
    return db_payment

def get_payments_by_user(db: Session, user_id: int):
    return db.query(models.Payment).filter(
        or_(
            models.Payment.from_user_id == user_id,
            models.Payment.to_user_id == user_id
        )
    ).all()
