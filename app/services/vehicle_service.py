from sqlalchemy.orm import Session
from typing import List, Optional

from ..repositories import VehicleRepository
from ..models import Vehicle
from .. import schemas

class VehicleService:
    def __init__(self, db: Session):
        self.db = db
        self.vehicle_repo = VehicleRepository(db)
    
    def create_vehicle(self, vehicle: schemas.VehicleCreate) -> Vehicle:
        """Create a new vehicle with validation"""
        return self.vehicle_repo.create(vehicle)
    
    def get_vehicle_by_id(self, vehicle_id: int) -> Optional[Vehicle]:
        """Get vehicle by ID"""
        return self.vehicle_repo.get_by_id(vehicle_id)
    
    def get_user_vehicles(self, user_id: int) -> List[Vehicle]:
        """Get all vehicles owned by a user"""
        return self.vehicle_repo.get_by_user_id(user_id)
    
    def update_vehicle(self, vehicle_id: int, vehicle_update: schemas.VehicleUpdate) -> Vehicle:
        """Update vehicle information"""
        return self.vehicle_repo.update(vehicle_id, vehicle_update)
    
    def delete_vehicle(self, vehicle_id: int) -> dict:
        """Delete a vehicle"""
        return self.vehicle_repo.delete(vehicle_id) 