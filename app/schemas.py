from pydantic import BaseModel, EmailStr, validator
from typing import Optional, List
from datetime import datetime
from enum import Enum
from decimal import Decimal

# Enums matching the database models
class UserTypeEnum(str, Enum):
    DRIVER = "driver"
    PASSENGER = "passenger"

class TransactionType(str, Enum):
    DEBIT = "debit"
    CREDIT = "credit"

class PaymentType(str, Enum):
    CASH = "cash"
    WALLET = "wallet"

class RideStatus(str, Enum):
    PENDING = "pending"
    ACTIVE = "active"
    CONFIRMED = "confirmed"
    COMPLETED = "completed"
    CANCELLED = "cancelled"

class RequestStatus(str, Enum):
    PENDING = "pending"
    ACCEPTED = "accepted"
    REJECTED = "rejected"
    CANCELLED = "cancelled"

class GenderPreference(str, Enum):
    ANY = "any"
    MALE = "male"
    FEMALE = "female"

# ============== USER SCHEMAS ==============
class UserBase(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr
    phone_no: Optional[str] = None
    user_type: Optional[UserTypeEnum] = None
    cnic: Optional[str] = None
    profile_picture: Optional[str] = None
    bio: Optional[str] = None
    driving_license: Optional[str] = None
    gender: Optional[str] = None

class UserCreate(UserBase):
    password: str
    user_type: UserTypeEnum

class UserUpdate(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    phone_no: Optional[str] = None
    user_type: Optional[UserTypeEnum] = None
    cnic: Optional[str] = None
    profile_picture: Optional[str] = None
    bio: Optional[str] = None
    driving_license: Optional[str] = None
    gender: Optional[str] = None

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class UserResponse(UserBase):
    id: int
    wallet: float
    average_rating: float
    created_at: datetime
    
    class Config:
        from_attributes = True

# New schemas for user management
class ProfileSetup(BaseModel):
    bio: Optional[str] = None
    profile_picture: Optional[str] = None
    gender: Optional[str] = None

class RoleSelection(BaseModel):
    user_type: UserTypeEnum

class ChangePassword(BaseModel):
    current_password: str
    new_password: str
    
    @validator('new_password')
    def validate_password(cls, v):
        if len(v) < 6:
            raise ValueError('Password must be at least 6 characters long')
        return v

class AddMoney(BaseModel):
    amount: float
    
    @validator('amount')
    def validate_amount(cls, v):
        if v <= 0:
            raise ValueError('Amount must be positive')
        return v

# ============== VEHICLE SCHEMAS ==============
class VehicleBase(BaseModel):
    model: Optional[str] = None
    name_make: Optional[str] = None
    color: Optional[str] = None
    no_plate: Optional[str] = None
    registration: Optional[str] = None

class VehicleCreate(VehicleBase):
    user_id: Optional[int] = None  # Will be set by controller

class VehicleUpdate(BaseModel):
    model: Optional[str] = None
    name_make: Optional[str] = None
    color: Optional[str] = None
    no_plate: Optional[str] = None
    registration: Optional[str] = None

class VehicleResponse(VehicleBase):
    id: int
    user_id: int
    created_at: datetime
    
    class Config:
        from_attributes = True

# ============== RIDE SCHEMAS ==============
class RideBase(BaseModel):
    timing: datetime
    source: str
    destination: str
    fare: float
    seats_offered: int
    ac: bool = False
    smoking: bool = False
    music: bool = False
    gender_preference: GenderPreference = GenderPreference.ANY

class RideCreate(RideBase):
    user_id: Optional[int] = None  # Will be set by controller

class RideUpdate(BaseModel):
    timing: Optional[datetime] = None
    source: Optional[str] = None
    destination: Optional[str] = None
    fare: Optional[float] = None
    seats_offered: Optional[int] = None
    ac: Optional[bool] = None
    smoking: Optional[bool] = None
    music: Optional[bool] = None
    gender_preference: Optional[GenderPreference] = None
    status: Optional[RideStatus] = None

class RideResponse(RideBase):
    id: int
    user_id: int
    status: RideStatus
    created_at: datetime
    
    class Config:
        from_attributes = True

class RideWithDriver(RideResponse):
    driver: UserResponse

# ============== RIDE REQUEST SCHEMAS ==============
class RideRequestBase(BaseModel):
    seats: int
    source: Optional[str] = None
    destination: Optional[str] = None
    ac: bool = False
    smoking: bool = False
    music: bool = False
    gender_preference: GenderPreference = GenderPreference.ANY

class RideRequestCreate(RideRequestBase):
    user_id: Optional[int] = None  # Will be set by controller
    ride_id: int

class RideRequestUpdate(BaseModel):
    status: Optional[RequestStatus] = None
    seats: Optional[int] = None

class RideRequestResponse(RideRequestBase):
    id: int
    user_id: int
    ride_id: int
    datetime: datetime
    status: RequestStatus
    
    class Config:
        from_attributes = True

class RideRequestWithDetails(RideRequestResponse):
    passenger: UserResponse
    ride: RideResponse

# ============== TRANSACTION SCHEMAS ==============
class TransactionBase(BaseModel):
    type: TransactionType
    amount: float

class TransactionCreate(TransactionBase):
    user_id: Optional[int] = None  # Will be set by controller
    ride_id: Optional[int] = None

class TransactionResponse(TransactionBase):
    id: int
    user_id: int
    ride_id: Optional[int] = None
    datetime: datetime
    
    class Config:
        from_attributes = True

# ============== RATINGS & REVIEWS SCHEMAS ==============
class RatingBase(BaseModel):
    stars: int
    text_review: Optional[str] = None
    
    @validator('stars')
    def validate_stars(cls, v):
        if v < 1 or v > 5:
            raise ValueError('Stars must be between 1 and 5')
        return v

class RatingCreate(RatingBase):
    reviewer_id: Optional[int] = None  # Will be set by controller
    reviewee_id: int

class RatingResponse(RatingBase):
    id: int
    reviewer_id: int
    reviewee_id: int
    created_at: datetime
    
    class Config:
        from_attributes = True

class RatingWithDetails(RatingResponse):
    reviewer: UserResponse
    reviewee: UserResponse

# New schema for rating after ride
class RateUserAfterRide(BaseModel):
    reviewee_id: int
    ride_id: int
    stars: int
    text_review: Optional[str] = None
    
    @validator('stars')
    def validate_stars(cls, v):
        if v < 1 or v > 5:
            raise ValueError('Stars must be between 1 and 5')
        return v

# ============== PAYMENT SCHEMAS ==============
class PaymentBase(BaseModel):
    type: PaymentType

class PaymentCreate(PaymentBase):
    transaction_id: int
    from_user_id: int
    to_user_id: int

class PaymentResponse(PaymentBase):
    id: int
    transaction_id: int
    from_user_id: int
    to_user_id: int
    created_at: datetime
    
    class Config:
        from_attributes = True

class PaymentWithDetails(PaymentResponse):
    transaction: TransactionResponse
    sender: UserResponse
    receiver: UserResponse

# ============== SEARCH AND FILTER SCHEMAS ==============
class RideSearchParams(BaseModel):
    source: Optional[str] = None
    destination: Optional[str] = None
    date: Optional[str] = None  # YYYY-MM-DD format
    min_seats: Optional[int] = None
    max_fare: Optional[float] = None
    min_fare: Optional[float] = None
    ac: Optional[bool] = None
    smoking: Optional[bool] = None
    music: Optional[bool] = None
    gender_preference: Optional[str] = None

# ============== UTILITY SCHEMAS ==============
class ApiResponse(BaseModel):
    success: bool
    message: str
    data: Optional[dict] = None

class PaginatedResponse(BaseModel):
    items: List[dict]
    total: int
    page: int
    per_page: int
    pages: int
