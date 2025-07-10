from sqlalchemy.orm import Session
from typing import List, Optional

from ..repositories import RideRequestRepository
from ..models import RideRequest
from .. import schemas

class RideRequestService:
    def __init__(self, db: Session):
        self.db = db
        self.ride_request_repo = RideRequestRepository(db)
    
    def create_ride_request(self, ride_request: schemas.RideRequestCreate) -> RideRequest:
        """Create a new ride request with validation"""
        return self.ride_request_repo.create(ride_request)
    
    def get_ride_request_by_id(self, request_id: int) -> Optional[RideRequest]:
        """Get ride request by ID"""
        return self.ride_request_repo.get_by_id(request_id)
    
    def get_user_ride_requests(self, user_id: int) -> List[RideRequest]:
        """Get all ride requests made by a user"""
        return self.ride_request_repo.get_by_user_id(user_id)
    
    def get_ride_requests_for_ride(self, ride_id: int) -> List[RideRequest]:
        """Get all requests for a specific ride"""
        return self.ride_request_repo.get_by_ride_id(ride_id)
    
    def accept_ride_request(self, request_id: int) -> RideRequest:
        """Accept a ride request"""
        return self.ride_request_repo.update_status(request_id, "accepted")
    
    def reject_ride_request(self, request_id: int) -> RideRequest:
        """Reject a ride request"""
        return self.ride_request_repo.update_status(request_id, "rejected")
    
    def complete_ride_request(self, request_id: int) -> RideRequest:
        """Mark a ride request as completed"""
        return self.ride_request_repo.update_status(request_id, "completed") 