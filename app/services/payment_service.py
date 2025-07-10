from sqlalchemy.orm import Session
from typing import List

from ..repositories import PaymentRepository
from ..models import Payment
from .. import schemas

class PaymentService:
    def __init__(self, db: Session):
        self.db = db
        self.payment_repo = PaymentRepository(db)
    
    def create_payment(self, payment: schemas.PaymentCreate) -> Payment:
        """Create a new payment with validation"""
        return self.payment_repo.create(payment)
    
    def get_user_payments(self, user_id: int) -> List[Payment]:
        """Get all payments for a user (sent and received)"""
        return self.payment_repo.get_by_user_id(user_id) 