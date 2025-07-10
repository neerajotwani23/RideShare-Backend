from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from jose import JWTError, jwt
from datetime import datetime, timedelta
import os

from ..services import UserService
from ..models import User
from .. import schemas
from ..database import SessionLocal

# Database dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# JWT Configuration
SECRET_KEY = os.getenv("SECRET_KEY", "your-secret-key-here")
# SECRET_KEY = "123ABCDEFGHIJKLMNOPQRSTWYZIKLUHHBJH"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

security = HTTPBearer()

class AuthController:
    def __init__(self):
        self.router = APIRouter(prefix="/auth", tags=["Authentication"])
        self._setup_routes()
    
    def _setup_routes(self):
        self.router.add_api_route("/register", self.register_user, methods=["POST"], response_model=schemas.UserResponse)
        self.router.add_api_route("/login", self.login_user, methods=["POST"])
        self.router.add_api_route("/me", self.get_current_user_info, methods=["GET"], response_model=schemas.UserResponse)
        self.router.add_api_route("/me", self.update_current_user, methods=["PUT"], response_model=schemas.UserResponse)
    
    @staticmethod
    def create_access_token(data: dict, expires_delta: timedelta = None):
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(minutes=15)
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
        return encoded_jwt
    
    @staticmethod
    def verify_token(credentials: HTTPAuthorizationCredentials = Depends(security)):
        try:

            payload = jwt.decode(credentials.credentials, SECRET_KEY, algorithms=[ALGORITHM])
            user_id: int = payload.get("sub")
            if user_id is None:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Could not validate credentials"
                )
            return user_id
        except JWTError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Could not validate credentials"
            )
    
    @staticmethod
    def get_current_user(
        user_id: int = Depends(verify_token),
        db: Session = Depends(get_db)
    ):
        user_service = UserService(db)
        user = user_service.get_user_by_id(user_id)
        if user is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="User not found"
            )
        return user
    
    def register_user(self, user: schemas.UserCreate, db: Session = Depends(get_db)):
        """Register a new user"""
        try:
            user_service = UserService(db)
            db_user = user_service.create_user(user)
            return db_user
        except HTTPException as e:
            raise e
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="An error occurred while creating the user"
            )
    
    def login_user(self, user_credentials: schemas.UserLogin, db: Session = Depends(get_db)):
        """Login user and return access token"""
        user_service = UserService(db)
        user = user_service.authenticate_user(user_credentials.email, user_credentials.password)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid email or password"
            )
        
        access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = self.create_access_token(
            data={"sub": str(user.id)}, expires_delta=access_token_expires
        )
        
        return {
            "access_token": access_token,
            "token_type": "bearer",
            "user": schemas.UserResponse.from_orm(user)
        }
    
    def get_current_user_info(self, current_user: User = Depends(get_current_user)):
        """Get current user information"""
        return current_user
    
    def update_current_user(
        self,
        user_update: schemas.UserUpdate,
        current_user: User = Depends(get_current_user),
        db: Session = Depends(get_db)
    ):
        """Update current user information"""
        user_service = UserService(db)
        return user_service.update_user(current_user.id, user_update) 