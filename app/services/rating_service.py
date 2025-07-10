from sqlalchemy.orm import Session
from typing import List

from ..repositories import RatingRepository, UserRepository
from ..models import RatingsReviews
from .. import schemas

class RatingService:
    def __init__(self, db: Session):
        self.db = db
        self.rating_repo = RatingRepository(db)
        self.user_repo = UserRepository(db)
    
    def create_rating(self, rating: schemas.RatingCreate) -> RatingsReviews:
        """Create a new rating and update user's average rating"""
        db_rating = self.rating_repo.create(rating)
        
        # Update the user's average rating
        self.user_repo.update_rating(rating.user_id)
        
        return db_rating
    
    def get_ride_ratings(self, ride_id: int) -> List[RatingsReviews]:
        """Get all ratings for a specific ride"""
        return self.rating_repo.get_by_ride_id(ride_id)
    
    def get_user_ratings(self, user_id: int) -> List[RatingsReviews]:
        """Get all ratings given by a user"""
        return self.rating_repo.get_by_user_id(user_id) 