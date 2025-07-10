from sqlalchemy.orm import Session
from typing import List, Optional
from fastapi import HTTPException, status

from ..models import Vehicle
from .. import schemas

class VehicleRepository:
    def __init__(self, db: Session):
        self.db = db
    
    def create(self, vehicle: schemas.VehicleCreate) -> Vehicle:
        # Check if plate number already exists
        existing_vehicle = self.db.query(Vehicle).filter(
            Vehicle.no_plate == vehicle.no_plate
        ).first()
        if existing_vehicle:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Vehicle with this plate number already exists"
            )
        
        db_vehicle = Vehicle(**vehicle.dict())
        self.db.add(db_vehicle)
        self.db.commit()
        self.db.refresh(db_vehicle)
        return db_vehicle
    
    def get_by_id(self, vehicle_id: int) -> Optional[Vehicle]:
        return self.db.query(Vehicle).filter(Vehicle.id == vehicle_id).first()
    
    def get_by_user_id(self, user_id: int) -> List[Vehicle]:
        return self.db.query(Vehicle).filter(Vehicle.user_id == user_id).all()
    
    def update(self, vehicle_id: int, vehicle_update: schemas.VehicleUpdate) -> Vehicle:
        db_vehicle = self.get_by_id(vehicle_id)
        if not db_vehicle:
            raise HTTPException(status_code=404, detail="Vehicle not found")
        
        update_data = vehicle_update.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_vehicle, field, value)
        
        self.db.commit()
        self.db.refresh(db_vehicle)
        return db_vehicle
    
    def delete(self, vehicle_id: int) -> dict:
        db_vehicle = self.get_by_id(vehicle_id)
        if not db_vehicle:
            raise HTTPException(status_code=404, detail="Vehicle not found")
        
        self.db.delete(db_vehicle)
        self.db.commit()
        return {"message": "Vehicle deleted successfully"} 