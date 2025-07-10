from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional

from ..services import RideService
from ..models import User, RideStatusEnum, GenderPreferenceEnum
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

class RideController:
    def __init__(self):
        self.router = APIRouter(prefix="/rides", tags=["Rides"])
        self._setup_routes()
    
    def _setup_routes(self):
        # Ride management
        self.router.add_api_route("/", self.create_ride, methods=["POST"], response_model=schemas.RideResponse)
        self.router.add_api_route("/search", self.search_rides, methods=["GET"], response_model=List[schemas.RideResponse])
        self.router.add_api_route("/my-rides", self.get_my_rides, methods=["GET"], response_model=List[schemas.RideResponse])
        self.router.add_api_route("/{ride_id}", self.get_ride, methods=["GET"], response_model=schemas.RideResponse)
        self.router.add_api_route("/{ride_id}", self.update_ride, methods=["PUT"], response_model=schemas.RideResponse)
        
        # Ride status management
        self.router.add_api_route("/{ride_id}/cancel", self.cancel_ride, methods=["PUT"], response_model=schemas.RideResponse)
        self.router.add_api_route("/{ride_id}/confirm", self.confirm_ride, methods=["PUT"], response_model=schemas.RideResponse)
        self.router.add_api_route("/{ride_id}/activate", self.activate_ride, methods=["PUT"], response_model=schemas.RideResponse)
        self.router.add_api_route("/{ride_id}/complete", self.complete_ride, methods=["PUT"], response_model=schemas.RideResponse)
        
        # Filtering
        self.router.add_api_route("/filter/upcoming", self.get_upcoming_rides, methods=["GET"], response_model=List[schemas.RideResponse])
        self.router.add_api_route("/filter/past", self.get_past_rides, methods=["GET"], response_model=List[schemas.RideResponse])
        self.router.add_api_route("/filter/by-status", self.get_rides_by_status, methods=["GET"], response_model=List[schemas.RideResponse])
    
    def create_ride(
        self,
        ride: schemas.RideCreate,
        current_user: User = Depends(AuthController.get_current_user),
        db: Session = Depends(get_db)
    ):
        """Create a new ride (Post Ride functionality)"""
        # Verify user is a driver
        if current_user.user_type.value != "driver":
            raise HTTPException(status_code=403, detail="Only drivers can create rides")
            
        ride_service = RideService(db)
        ride.user_id = current_user.id
        return ride_service.create_ride(ride)
    
    def search_rides(
        self,
        source: Optional[str] = Query(None, description="Source location"),
        destination: Optional[str] = Query(None, description="Destination location"),
        date: Optional[str] = Query(None, description="Date (YYYY-MM-DD)"),
        min_seats: Optional[int] = Query(None, description="Minimum seats required"),
        max_fare: Optional[float] = Query(None, description="Maximum fare"),
        min_fare: Optional[float] = Query(None, description="Minimum fare"),
        ac: Optional[bool] = Query(None, description="AC required"),
        smoking: Optional[bool] = Query(None, description="Smoking allowed"),
        music: Optional[bool] = Query(None, description="Music allowed"),
        gender_preference: Optional[str] = Query(None, description="Gender preference: any, male, female"),
        skip: int = Query(0, description="Number of records to skip"),
        limit: int = Query(10, description="Number of records to return"),
        db: Session = Depends(get_db)
    ):
        """Search for available rides (Find Ride functionality)"""
        search_params = schemas.RideSearchParams(
            source=source,
            destination=destination,
            date=date,
            min_seats=min_seats,
            max_fare=max_fare,
            min_fare=min_fare,
            ac=ac,
            smoking=smoking,
            music=music,
            gender_preference=gender_preference
        )
        ride_service = RideService(db)
        return ride_service.search_rides(search_params, skip, limit)
    
    def get_my_rides(
        self,
        current_user: User = Depends(AuthController.get_current_user),
        db: Session = Depends(get_db)
    ):
        """Get current user's rides"""
        ride_service = RideService(db)
        return ride_service.get_user_rides(current_user.id)
    
    def get_ride(
        self,
        ride_id: int,
        db: Session = Depends(get_db)
    ):
        """Get ride details by ID"""
        ride_service = RideService(db)
        ride = ride_service.get_ride_by_id(ride_id)
        if not ride:
            raise HTTPException(status_code=404, detail="Ride not found")
        return ride
    
    def update_ride(
        self,
        ride_id: int,
        ride_update: schemas.RideUpdate,
        current_user: User = Depends(AuthController.get_current_user),
        db: Session = Depends(get_db)
    ):
        """Update a ride"""
        ride_service = RideService(db)
        
        # Check if ride belongs to current user
        ride = ride_service.get_ride_by_id(ride_id)
        if not ride or ride.user_id != current_user.id:
            raise HTTPException(status_code=404, detail="Ride not found")
        
        return ride_service.update_ride(ride_id, ride_update)
    
    def cancel_ride(
        self,
        ride_id: int,
        current_user: User = Depends(AuthController.get_current_user),
        db: Session = Depends(get_db)
    ):
        """Cancel a ride"""
        ride_service = RideService(db)
        
        # Check if ride belongs to current user
        ride = ride_service.get_ride_by_id(ride_id)
        if not ride or ride.user_id != current_user.id:
            raise HTTPException(status_code=404, detail="Ride not found")
        
        return ride_service.update_ride_status(ride_id, RideStatusEnum.CANCELLED)
    
    def confirm_ride(
        self,
        ride_id: int,
        current_user: User = Depends(AuthController.get_current_user),
        db: Session = Depends(get_db)
    ):
        """Confirm a ride"""
        ride_service = RideService(db)
        
        # Check if ride belongs to current user
        ride = ride_service.get_ride_by_id(ride_id)
        if not ride or ride.user_id != current_user.id:
            raise HTTPException(status_code=404, detail="Ride not found")
        
        return ride_service.update_ride_status(ride_id, RideStatusEnum.CONFIRMED)
    
    def activate_ride(
        self,
        ride_id: int,
        current_user: User = Depends(AuthController.get_current_user),
        db: Session = Depends(get_db)
    ):
        """Activate a ride"""
        ride_service = RideService(db)
        
        # Check if ride belongs to current user
        ride = ride_service.get_ride_by_id(ride_id)
        if not ride or ride.user_id != current_user.id:
            raise HTTPException(status_code=404, detail="Ride not found")
        
        return ride_service.update_ride_status(ride_id, RideStatusEnum.ACTIVE)
    
    def complete_ride(
        self,
        ride_id: int,
        current_user: User = Depends(AuthController.get_current_user),
        db: Session = Depends(get_db)
    ):
        """Mark a ride as completed"""
        ride_service = RideService(db)
        
        # Check if ride belongs to current user
        ride = ride_service.get_ride_by_id(ride_id)
        if not ride or ride.user_id != current_user.id:
            raise HTTPException(status_code=404, detail="Ride not found")
        
        return ride_service.update_ride_status(ride_id, RideStatusEnum.COMPLETED)
    
    def get_upcoming_rides(
        self,
        current_user: User = Depends(AuthController.get_current_user),
        db: Session = Depends(get_db)
    ):
        """Get upcoming rides for MyRides screen"""
        ride_service = RideService(db)
        return ride_service.get_upcoming_rides(current_user.id)
    
    def get_past_rides(
        self,
        current_user: User = Depends(AuthController.get_current_user),
        db: Session = Depends(get_db)
    ):
        """Get past rides for MyRides screen"""
        ride_service = RideService(db)
        return ride_service.get_past_rides(current_user.id)
    
    def get_rides_by_status(
        self,
        status: str = Query(..., description="Ride status: pending, active, confirmed, completed, cancelled"),
        current_user: User = Depends(AuthController.get_current_user),
        db: Session = Depends(get_db)
    ):
        """Filter rides by status"""
        try:
            ride_status = RideStatusEnum(status)
        except ValueError:
            raise HTTPException(status_code=400, detail="Invalid ride status")
            
        ride_service = RideService(db)
        return ride_service.get_rides_by_status(current_user.id, ride_status) 