from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
import os

from .models import Base
from .database import engine, SessionLocal
from .controllers import (
    AuthController,
    UserController,
    VehicleController,
    RideController,
    RideRequestController,
    TransactionController,
    RatingController,
    PaymentController
)

# Database dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Create database tables
Base.metadata.create_all(bind=engine)

# FastAPI app configuration
app = FastAPI(
    title="RideShare API",
    description="A comprehensive rideshare platform API with user management, ride booking, payments, and ratings",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure this based on your frontend domains
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize and include all controllers
auth_controller = AuthController()
user_controller = UserController()
vehicle_controller = VehicleController()
ride_controller = RideController()
ride_request_controller = RideRequestController()
transaction_controller = TransactionController()
rating_controller = RatingController()
payment_controller = PaymentController()

# Include all routers
app.include_router(auth_controller.router)
app.include_router(user_controller.router)
app.include_router(vehicle_controller.router)
app.include_router(ride_controller.router)
app.include_router(ride_request_controller.router)
app.include_router(transaction_controller.router)
app.include_router(rating_controller.router)
app.include_router(payment_controller.router)

@app.get("/")
def read_root():
    """Root endpoint with API information"""
    return {
        "message": "Welcome to the RideShare API",
        "version": "1.0.0",
        "docs": "/docs",
        "redoc": "/redoc",
        "app_features": [
            "User Authentication & Role Selection",
            "Profile Management & Onboarding", 
            "Vehicle Registration (Drivers)",
            "Post & Search Rides",
            "Ride Request System",
            "Wallet & Payment Processing",
            "User-to-User Rating System",
            "Ride History & Filtering"
        ],
        "endpoints": {
            "auth": "/auth (login, register, reset password)",
            "users": "/users (profile, role selection, wallet)",
            "vehicles": "/vehicles (vehicle management for drivers)",
            "rides": "/rides (post ride, search, my rides)",
            "ride_requests": "/ride-requests (book rides, manage requests)",
            "transactions": "/transactions (wallet transactions)",
            "ratings": "/ratings (user reviews and ratings)",
            "payments": "/payments (payment processing)"
        },
        "app_screens_supported": [
            "SplashScreen, LoginScreen, SignupScreen",
            "RoleSelectionScreen, ProfileSetupScreen",
            "HomeScreen, FindRideScreen, SuggestedRidesScreen",
            "PostRideScreen, MyRidesScreen, RideDetailsScreen",
            "WalletScreen, VehicleDetailsScreen",
            "RateRideScreen, ProfileScreen, SettingsScreen"
        ]
    }

@app.get("/health")
def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "message": "RideShare API is running"}

@app.get("/info")
def get_api_info():
    """Get API configuration information"""
    return {
        "database_connected": True,
        "environment": os.getenv("ENVIRONMENT", "development"),
        "api_version": "1.0.0",
        "architecture": "Layered Architecture (Controller -> Service -> Repository)",
        "database_schema": "MySQL with proper enums and relationships",
        "features": {
            "authentication": "JWT-based with role-based access",
            "user_types": ["driver", "passenger"],
            "ride_statuses": ["pending", "active", "confirmed", "completed", "cancelled"],
            "payment_types": ["cash", "wallet"],
            "rating_system": "User-to-user 5-star rating with reviews"
        }
    }
