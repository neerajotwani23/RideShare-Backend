from sqlalchemy.orm import Session
from sqlalchemy import func
from datetime import datetime
from typing import List, Optional
from fastapi import HTTPException

from ..models import Ride
from .. import schemas

class RideRepository:
    def __init__(self, db: Session):
        self.db = db
    
    def create(self, ride: schemas.RideCreate) -> Ride:
        db_ride = Ride(**ride.dict())
        self.db.add(db_ride)
        self.db.commit()
        self.db.refresh(db_ride)
        return db_ride
    
    def get_by_id(self, ride_id: int) -> Optional[Ride]:
        return self.db.query(Ride).filter(Ride.id == ride_id).first()
    
    def get_by_user_id(self, user_id: int) -> List[Ride]:
        return self.db.query(Ride).filter(Ride.user_id == user_id).all()
    
    def search(self, search_params: schemas.RideSearchParams, skip: int = 0, limit: int = 10) -> List[Ride]:
        query = self.db.query(Ride).filter(Ride.status == "active")
        
        if search_params.source:
            query = query.filter(Ride.source.ilike(f"%{search_params.source}%"))
        if search_params.destination:
            query = query.filter(Ride.destination.ilike(f"%{search_params.destination}%"))
        if search_params.date:
            search_date = datetime.strptime(search_params.date, "%Y-%m-%d").date()
            query = query.filter(func.date(Ride.timing) == search_date)
        if search_params.min_seats:
            query = query.filter(Ride.seats_offered >= search_params.min_seats)
        if search_params.max_fare:
            query = query.filter(Ride.fare <= search_params.max_fare)
        if search_params.ac is not None:
            query = query.filter(Ride.ac == search_params.ac)
        if search_params.smoking is not None:
            query = query.filter(Ride.smoking == search_params.smoking)
        if search_params.music is not None:
            query = query.filter(Ride.music == search_params.music)
        if search_params.gender_preference is not None:
            query = query.filter(Ride.gender_preference == search_params.gender_preference)
        
        return query.offset(skip).limit(limit).all()
    
    def update(self, ride_id: int, ride_update: schemas.RideUpdate) -> Ride:
        db_ride = self.get_by_id(ride_id)
        if not db_ride:
            raise HTTPException(status_code=404, detail="Ride not found")
        
        update_data = ride_update.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_ride, field, value)
        
        self.db.commit()
        self.db.refresh(db_ride)
        return db_ride
    
    def cancel(self, ride_id: int) -> Ride:
        db_ride = self.get_by_id(ride_id)
        if not db_ride:
            raise HTTPException(status_code=404, detail="Ride not found")
        
        db_ride.status = "cancelled"
        self.db.commit()
        self.db.refresh(db_ride)
        return db_ride 