from sqlalchemy.orm import Session
from typing import Optional

from ..repositories import UserRepository
from ..models import User
from .. import schemas

class UserService:
    def __init__(self, db: Session):
        self.db = db
        self.user_repo = UserRepository(db)
    
    def create_user(self, user: schemas.UserCreate) -> User:
        """Create a new user with validation"""
        return self.user_repo.create(user)
    
    def authenticate_user(self, email: str, password: str) -> Optional[User]:
        """Authenticate user credentials"""
        return self.user_repo.authenticate(email, password)
    
    def get_user_by_id(self, user_id: int) -> Optional[User]:
        """Get user by ID"""
        return self.user_repo.get_by_id(user_id)
    
    def get_user_by_email(self, email: str) -> Optional[User]:
        """Get user by email"""
        return self.user_repo.get_by_email(email)
    
    def update_user(self, user_id: int, user_update: schemas.UserUpdate) -> User:
        """Update user information"""
        return self.user_repo.update(user_id, user_update)
    
    def update_wallet_balance(self, user_id: int, amount: float) -> User:
        """Update user wallet balance"""
        return self.user_repo.update_wallet(user_id, amount)
    
    def recalculate_user_rating(self, user_id: int) -> User:
        """Recalculate and update user's average rating"""
        return self.user_repo.update_rating(user_id) 