from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import Optional
from fastapi import HTTPException, status
from passlib.context import CryptContext

from ..models import User
from .. import schemas

# Password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class UserRepository:
    def __init__(self, db: Session):
        self.db = db
    
    @staticmethod
    def get_password_hash(password: str) -> str:
        return pwd_context.hash(password)
    
    @staticmethod
    def verify_password(plain_password: str, hashed_password: str) -> bool:
        return pwd_context.verify(plain_password, hashed_password)
    
    def create(self, user: schemas.UserCreate) -> User:
        # Check if email already exists
        db_user = self.db.query(User).filter(User.email == user.email).first()
        if db_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered"
            )
        
        # Hash password and create user
        hashed_password = self.get_password_hash(user.password)
        user_data = user.dict()
        user_data["password"] = hashed_password
        
        db_user = User(**user_data)
        self.db.add(db_user)
        self.db.commit()
        self.db.refresh(db_user)
        return db_user
    
    def get_by_id(self, user_id: int) -> Optional[User]:
        return self.db.query(User).filter(User.id == user_id).first()
    
    def get_by_email(self, email: str) -> Optional[User]:
        return self.db.query(User).filter(User.email == email).first()
    
    def authenticate(self, email: str, password: str) -> Optional[User]:
        user = self.get_by_email(email)
        if not user or not self.verify_password(password, user.password):
            return None
        return user
    
    def update(self, user_id: int, user_update: schemas.UserUpdate) -> User:
        db_user = self.get_by_id(user_id)
        if not db_user:
            raise HTTPException(status_code=404, detail="User not found")
        
        update_data = user_update.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_user, field, value)
        
        self.db.commit()
        self.db.refresh(db_user)
        return db_user
    
    def update_wallet(self, user_id: int, amount: float) -> User:
        db_user = self.get_by_id(user_id)
        if not db_user:
            raise HTTPException(status_code=404, detail="User not found")
        
        db_user.wallet += amount
        self.db.commit()
        self.db.refresh(db_user)
        return db_user
    
    def update_rating(self, user_id: int) -> User:
        """Recalculate and update user's average rating"""
        from ..models import RatingsReviews
        
        avg_rating = self.db.query(func.avg(RatingsReviews.stars)).filter(
            RatingsReviews.user_id == user_id
        ).scalar()
        
        db_user = self.get_by_id(user_id)
        if db_user:
            db_user.average_rating = float(avg_rating) if avg_rating else 0.0
            self.db.commit()
            self.db.refresh(db_user)
        return db_user 