from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from ..services import RideRequestService
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

class RideRequestController:
    def __init__(self):
        self.router = APIRouter(prefix="/ride-requests", tags=["Ride Requests"])
        self._setup_routes()
    
    def _setup_routes(self):
        self.router.add_api_route("/", self.create_ride_request, methods=["POST"], response_model=schemas.RideRequestResponse)
        self.router.add_api_route("/my-requests", self.get_my_ride_requests, methods=["GET"], response_model=List[schemas.RideRequestResponse])
        self.router.add_api_route("/ride/{ride_id}", self.get_ride_requests, methods=["GET"], response_model=List[schemas.RideRequestResponse])
        self.router.add_api_route("/{request_id}/accept", self.accept_ride_request, methods=["PUT"], response_model=schemas.RideRequestResponse)
        self.router.add_api_route("/{request_id}/reject", self.reject_ride_request, methods=["PUT"], response_model=schemas.RideRequestResponse)
        self.router.add_api_route("/{request_id}/complete", self.complete_ride_request, methods=["PUT"], response_model=schemas.RideRequestResponse)
    
    def create_ride_request(
        self,
        ride_request: schemas.RideRequestCreate,
        current_user: User = Depends(AuthController.get_current_user),
        db: Session = Depends(get_db)
    ):
        """Create a new ride request"""
        ride_request_service = RideRequestService(db)
        ride_request.user_id = current_user.id
        return ride_request_service.create_ride_request(ride_request)
    
    def get_my_ride_requests(
        self,
        current_user: User = Depends(AuthController.get_current_user),
        db: Session = Depends(get_db)
    ):
        """Get current user's ride requests"""
        ride_request_service = RideRequestService(db)
        return ride_request_service.get_user_ride_requests(current_user.id)
    
    def get_ride_requests(
        self,
        ride_id: int,
        current_user: User = Depends(AuthController.get_current_user),
        db: Session = Depends(get_db)
    ):
        """Get all requests for a specific ride (only for ride owner)"""
        ride_request_service = RideRequestService(db)
        
        # Import here to avoid circular imports
        from ..services import RideService
        ride_service = RideService(db)
        
        # Check if current user owns the ride
        ride = ride_service.get_ride_by_id(ride_id)
        if not ride or ride.user_id != current_user.id:
            raise HTTPException(status_code=403, detail="Access denied")
        
        return ride_request_service.get_ride_requests_for_ride(ride_id)
    
    def accept_ride_request(
        self,
        request_id: int,
        current_user: User = Depends(AuthController.get_current_user),
        db: Session = Depends(get_db)
    ):
        """Accept a ride request"""
        ride_request_service = RideRequestService(db)
        
        # Get the ride request
        ride_request = ride_request_service.get_ride_request_by_id(request_id)
        if not ride_request:
            raise HTTPException(status_code=404, detail="Ride request not found")
        
        # Import here to avoid circular imports
        from ..services import RideService
        ride_service = RideService(db)
        
        # Check if current user owns the ride
        ride = ride_service.get_ride_by_id(ride_request.ride_id)
        if not ride or ride.user_id != current_user.id:
            raise HTTPException(status_code=403, detail="Access denied")
        
        return ride_request_service.accept_ride_request(request_id)
    
    def reject_ride_request(
        self,
        request_id: int,
        current_user: User = Depends(AuthController.get_current_user),
        db: Session = Depends(get_db)
    ):
        """Reject a ride request"""
        ride_request_service = RideRequestService(db)
        
        # Get the ride request
        ride_request = ride_request_service.get_ride_request_by_id(request_id)
        if not ride_request:
            raise HTTPException(status_code=404, detail="Ride request not found")
        
        # Import here to avoid circular imports
        from ..services import RideService
        ride_service = RideService(db)
        
        # Check if current user owns the ride
        ride = ride_service.get_ride_by_id(ride_request.ride_id)
        if not ride or ride.user_id != current_user.id:
            raise HTTPException(status_code=403, detail="Access denied")
        
        return ride_request_service.reject_ride_request(request_id)
    
    def complete_ride_request(
        self,
        request_id: int,
        current_user: User = Depends(AuthController.get_current_user),
        db: Session = Depends(get_db)
    ):
        """Complete a ride request"""
        ride_request_service = RideRequestService(db)
        
        # Get the ride request
        ride_request = ride_request_service.get_ride_request_by_id(request_id)
        if not ride_request:
            raise HTTPException(status_code=404, detail="Ride request not found")
        
        # Import here to avoid circular imports
        from ..services import RideService
        ride_service = RideService(db)
        
        # Check if current user owns the ride
        ride = ride_service.get_ride_by_id(ride_request.ride_id)
        if not ride or ride.user_id != current_user.id:
            raise HTTPException(status_code=403, detail="Access denied")
        
        return ride_request_service.complete_ride_request(request_id) 