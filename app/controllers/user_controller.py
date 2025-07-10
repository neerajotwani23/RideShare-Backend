from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from sqlalchemy.orm import Session
from typing import List, Optional

from ..services import UserService
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

class UserController:
    def __init__(self):
        self.router = APIRouter(prefix="/users", tags=["User Management"])
        self._setup_routes()
    
    def _setup_routes(self):
        # Profile management
        self.router.add_api_route("/profile", self.get_profile, methods=["GET"], response_model=schemas.UserResponse)
        self.router.add_api_route("/profile", self.update_profile, methods=["PUT"], response_model=schemas.UserResponse)
        self.router.add_api_route("/profile/setup", self.profile_setup, methods=["POST"], response_model=schemas.UserResponse)
        self.router.add_api_route("/profile/avatar", self.upload_avatar, methods=["POST"])
        
        # Role selection
        self.router.add_api_route("/role", self.select_role, methods=["PUT"], response_model=schemas.UserResponse)
        
        # Password management
        self.router.add_api_route("/change-password", self.change_password, methods=["PUT"])
        
        # Wallet management
        self.router.add_api_route("/wallet/balance", self.get_wallet_balance, methods=["GET"])
        self.router.add_api_route("/wallet/add-money", self.add_money_to_wallet, methods=["POST"], response_model=schemas.UserResponse)
        
        # User reviews and ratings
        self.router.add_api_route("/reviews/given", self.get_reviews_given, methods=["GET"], response_model=List[schemas.RatingResponse])
        self.router.add_api_route("/reviews/received", self.get_reviews_received, methods=["GET"], response_model=List[schemas.RatingResponse])
        
        # User search (for admin or finding users to rate)
        self.router.add_api_route("/search", self.search_users, methods=["GET"], response_model=List[schemas.UserResponse])
    
    def get_profile(
        self,
        current_user: User = Depends(AuthController.get_current_user)
    ):
        """Get current user's profile information"""
        return current_user
    
    def update_profile(
        self,
        profile_update: schemas.UserUpdate,
        current_user: User = Depends(AuthController.get_current_user),
        db: Session = Depends(get_db)
    ):
        """Update user profile information"""
        user_service = UserService(db)
        return user_service.update_user(current_user.id, profile_update)
    
    def profile_setup(
        self,
        profile_data: schemas.ProfileSetup,
        current_user: User = Depends(AuthController.get_current_user),
        db: Session = Depends(get_db)
    ):
        """Complete profile setup for new users"""
        user_service = UserService(db)
        user_update = schemas.UserUpdate(
            bio=profile_data.bio,
            profile_picture=profile_data.profile_picture,
            gender=profile_data.gender
        )
        return user_service.update_user(current_user.id, user_update)
    
    def upload_avatar(
        self,
        file: UploadFile = File(...),
        current_user: User = Depends(AuthController.get_current_user),
        db: Session = Depends(get_db)
    ):
        """Upload user profile picture"""
        # In a real implementation, you would save the file to cloud storage
        # For now, we'll just simulate saving the filename
        filename = f"avatars/{current_user.id}_{file.filename}"
        
        user_service = UserService(db)
        user_update = schemas.UserUpdate(profile_picture=filename)
        updated_user = user_service.update_user(current_user.id, user_update)
        
        return {"message": "Avatar uploaded successfully", "filename": filename}
    
    def select_role(
        self,
        role_data: schemas.RoleSelection,
        current_user: User = Depends(AuthController.get_current_user),
        db: Session = Depends(get_db)
    ):
        """Select user role (driver or passenger)"""
        user_service = UserService(db)
        user_update = schemas.UserUpdate(user_type=role_data.user_type)
        return user_service.update_user(current_user.id, user_update)
    
    def change_password(
        self,
        password_data: schemas.ChangePassword,
        current_user: User = Depends(AuthController.get_current_user),
        db: Session = Depends(get_db)
    ):
        """Change user password"""
        user_service = UserService(db)
        
        # Verify current password
        if not user_service.verify_password(password_data.current_password, current_user.password):
            raise HTTPException(status_code=400, detail="Invalid current password")
        
        # Update password
        user_service.update_password(current_user.id, password_data.new_password)
        return {"message": "Password updated successfully"}
    
    def get_wallet_balance(
        self,
        current_user: User = Depends(AuthController.get_current_user)
    ):
        """Get current wallet balance"""
        return {"balance": float(current_user.wallet)}
    
    def add_money_to_wallet(
        self,
        wallet_data: schemas.AddMoney,
        current_user: User = Depends(AuthController.get_current_user),
        db: Session = Depends(get_db)
    ):
        """Add money to user wallet"""
        user_service = UserService(db)
        return user_service.update_wallet_balance(current_user.id, wallet_data.amount)
    
    def get_reviews_given(
        self,
        current_user: User = Depends(AuthController.get_current_user),
        db: Session = Depends(get_db)
    ):
        """Get all reviews given by current user"""
        from ..services import RatingService
        rating_service = RatingService(db)
        return rating_service.get_reviews_given_by_user(current_user.id)
    
    def get_reviews_received(
        self,
        current_user: User = Depends(AuthController.get_current_user),
        db: Session = Depends(get_db)
    ):
        """Get all reviews received by current user"""
        from ..services import RatingService
        rating_service = RatingService(db)
        return rating_service.get_reviews_received_by_user(current_user.id)
    
    def search_users(
        self,
        name: Optional[str] = None,
        email: Optional[str] = None,
        current_user: User = Depends(AuthController.get_current_user),
        db: Session = Depends(get_db)
    ):
        """Search users by name or email (for rating purposes)"""
        user_service = UserService(db)
        return user_service.search_users(name=name, email=email) 