from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List

from ..services import PaymentService
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

class PaymentController:
    def __init__(self):
        self.router = APIRouter(prefix="/payments", tags=["Payments"])
        self._setup_routes()
    
    def _setup_routes(self):
        self.router.add_api_route("/", self.create_payment, methods=["POST"], response_model=schemas.PaymentResponse)
        self.router.add_api_route("/my-payments", self.get_my_payments, methods=["GET"], response_model=List[schemas.PaymentResponse])
    
    def create_payment(
        self,
        payment: schemas.PaymentCreate,
        current_user: User = Depends(AuthController.get_current_user),
        db: Session = Depends(get_db)
    ):
        """Create a new payment"""
        payment_service = PaymentService(db)
        return payment_service.create_payment(payment)
    
    def get_my_payments(
        self,
        current_user: User = Depends(AuthController.get_current_user),
        db: Session = Depends(get_db)
    ):
        """Get current user's payments (sent and received)"""
        payment_service = PaymentService(db)
        return payment_service.get_user_payments(current_user.id) 