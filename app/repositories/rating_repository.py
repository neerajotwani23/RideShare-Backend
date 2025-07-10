from sqlalchemy.orm import Session
from typing import List
from fastapi import HTTPException

from ..models import RatingsReviews, Ride
from .. import schemas

class RatingRepository:
    def __init__(self, db: Session):
        self.db = db
    
    def create(self, rating: schemas.RatingCreate) -> RatingsReviews:
        # Check if user already rated this ride
        existing_rating = self.db.query(RatingsReviews).filter(
            RatingsReviews.user_id == rating.user_id,
            RatingsReviews.ride_id == rating.ride_id
        ).first()
        
        if existing_rating:
            raise HTTPException(
                status_code=400,
                detail="You have already rated this ride"
            )
        
        # Check if ride exists and is completed
        ride = self.db.query(Ride).filter(Ride.id == rating.ride_id).first()
        if not ride:
            raise HTTPException(status_code=404, detail="Ride not found")
        
        if ride.status != "completed":
            raise HTTPException(
                status_code=400,
                detail="You can only rate completed rides"
            )
        
        db_rating = RatingsReviews(**rating.dict())
        self.db.add(db_rating)
        self.db.commit()
        self.db.refresh(db_rating)
        return db_rating
    
    def get_by_ride_id(self, ride_id: int) -> List[RatingsReviews]:
        return self.db.query(RatingsReviews).filter(RatingsReviews.ride_id == ride_id).all()
    
    def get_by_user_id(self, user_id: int) -> List[RatingsReviews]:
        return self.db.query(RatingsReviews).filter(RatingsReviews.user_id == user_id).all() 