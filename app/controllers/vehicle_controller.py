from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from ..services import VehicleService
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

class VehicleController:
    def __init__(self):
        self.router = APIRouter(prefix="/vehicles", tags=["Vehicles"])
        self._setup_routes()
    
    def _setup_routes(self):
        self.router.add_api_route("/", self.create_vehicle, methods=["POST"], response_model=schemas.VehicleResponse)
        self.router.add_api_route("/my-vehicles", self.get_my_vehicles, methods=["GET"], response_model=List[schemas.VehicleResponse])
        self.router.add_api_route("/{vehicle_id}", self.update_vehicle, methods=["PUT"], response_model=schemas.VehicleResponse)
        self.router.add_api_route("/{vehicle_id}", self.delete_vehicle, methods=["DELETE"])
    
    def create_vehicle(
        self,
        vehicle: schemas.VehicleCreate,
        current_user: User = Depends(AuthController.get_current_user),
        db: Session = Depends(get_db)
    ):
        """Create a new vehicle"""
        vehicle_service = VehicleService(db)
        vehicle.user_id = current_user.id
        return vehicle_service.create_vehicle(vehicle)
    
    def get_my_vehicles(
        self,
        current_user: User = Depends(AuthController.get_current_user),
        db: Session = Depends(get_db)
    ):
        """Get current user's vehicles"""
        vehicle_service = VehicleService(db)
        return vehicle_service.get_user_vehicles(current_user.id)
    
    def update_vehicle(
        self,
        vehicle_id: int,
        vehicle_update: schemas.VehicleUpdate,
        current_user: User = Depends(AuthController.get_current_user),
        db: Session = Depends(get_db)
    ):
        """Update a vehicle"""
        vehicle_service = VehicleService(db)
        
        # Check if vehicle belongs to current user
        vehicle = vehicle_service.get_vehicle_by_id(vehicle_id)
        if not vehicle or vehicle.user_id != current_user.id:
            raise HTTPException(status_code=404, detail="Vehicle not found")
        
        return vehicle_service.update_vehicle(vehicle_id, vehicle_update)
    
    def delete_vehicle(
        self,
        vehicle_id: int,
        current_user: User = Depends(AuthController.get_current_user),
        db: Session = Depends(get_db)
    ):
        """Delete a vehicle"""
        vehicle_service = VehicleService(db)
        
        # Check if vehicle belongs to current user
        vehicle = vehicle_service.get_vehicle_by_id(vehicle_id)
        if not vehicle or vehicle.user_id != current_user.id:
            raise HTTPException(status_code=404, detail="Vehicle not found")
        
        return vehicle_service.delete_vehicle(vehicle_id) 