from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from ..services import RatingService
from ..models import User
from .. import schemas
from ..database import SessionLocal
from .auth_controller import AuthController

# Database dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

class RatingController:
    def __init__(self):
        self.router = APIRouter(prefix="/ratings", tags=["Ratings & Reviews"])
        self._setup_routes()
    
    def _setup_routes(self):
        # Rating management
        self.router.add_api_route("/", self.create_rating, methods=["POST"], response_model=schemas.RatingResponse)
        self.router.add_api_route("/my-reviews/given", self.get_reviews_given, methods=["GET"], response_model=List[schemas.RatingResponse])
        self.router.add_api_route("/my-reviews/received", self.get_reviews_received, methods=["GET"], response_model=List[schemas.RatingResponse])
        
        # User ratings
        self.router.add_api_route("/user/{user_id}/reviews", self.get_user_reviews, methods=["GET"], response_model=List[schemas.RatingResponse])
        self.router.add_api_route("/user/{user_id}/average", self.get_user_average_rating, methods=["GET"])
        
        # Rate user after ride
        self.router.add_api_route("/rate-user", self.rate_user_after_ride, methods=["POST"], response_model=schemas.RatingResponse)
    
    def create_rating(
        self,
        rating: schemas.RatingCreate,
        current_user: User = Depends(AuthController.get_current_user),
        db: Session = Depends(get_db)
    ):
        """Create a new rating/review for another user"""
        rating_service = RatingService(db)
        rating.reviewer_id = current_user.id
        return rating_service.create_rating(rating)
    
    def get_reviews_given(
        self,
        current_user: User = Depends(AuthController.get_current_user),
        db: Session = Depends(get_db)
    ):
        """Get all reviews given by current user"""
        rating_service = RatingService(db)
        return rating_service.get_reviews_given_by_user(current_user.id)
    
    def get_reviews_received(
        self,
        current_user: User = Depends(AuthController.get_current_user),
        db: Session = Depends(get_db)
    ):
        """Get all reviews received by current user"""
        rating_service = RatingService(db)
        return rating_service.get_reviews_received_by_user(current_user.id)
    
    def get_user_reviews(
        self,
        user_id: int,
        db: Session = Depends(get_db)
    ):
        """Get all reviews for a specific user (public endpoint)"""
        rating_service = RatingService(db)
        return rating_service.get_reviews_received_by_user(user_id)
    
    def get_user_average_rating(
        self,
        user_id: int,
        db: Session = Depends(get_db)
    ):
        """Get average rating for a specific user"""
        rating_service = RatingService(db)
        average_rating = rating_service.calculate_user_average_rating(user_id)
        return {"user_id": user_id, "average_rating": average_rating}
    
    def rate_user_after_ride(
        self,
        rating_data: schemas.RateUserAfterRide,
        current_user: User = Depends(AuthController.get_current_user),
        db: Session = Depends(get_db)
    ):
        """Rate another user after completing a ride together"""
        rating_service = RatingService(db)
        
        # Verify that the current user and the rated user were part of the same ride
        # This adds extra validation for ride-based ratings
        if not rating_service.verify_ride_participation(current_user.id, rating_data.reviewee_id, rating_data.ride_id):
            raise HTTPException(status_code=400, detail="You can only rate users you've shared a ride with")
        
        rating = schemas.RatingCreate(
            reviewer_id=current_user.id,
            reviewee_id=rating_data.reviewee_id,
            stars=rating_data.stars,
            text_review=rating_data.text_review
        )
        
        return rating_service.create_rating(rating) 