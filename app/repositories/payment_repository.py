from sqlalchemy.orm import Session
from typing import List
from fastapi import HTTPException

from ..models import Payment, Transaction, User
from .. import schemas

class PaymentRepository:
    def __init__(self, db: Session):
        self.db = db
    
    def create(self, payment: schemas.PaymentCreate) -> Payment:
        # Verify transaction exists
        transaction = self.db.query(Transaction).filter(
            Transaction.id == payment.transaction_id
        ).first()
        if not transaction:
            raise HTTPException(status_code=404, detail="Transaction not found")
        
        # Verify users exist
        sender = self.db.query(User).filter(User.id == payment.from_user_id).first()
        receiver = self.db.query(User).filter(User.id == payment.to_user_id).first()
        
        if not sender or not receiver:
            raise HTTPException(status_code=404, detail="User not found")
        
        db_payment = Payment(**payment.dict())
        self.db.add(db_payment)
        self.db.commit()
        self.db.refresh(db_payment)
        return db_payment
    
    def get_by_user_id(self, user_id: int) -> List[Payment]:
        return self.db.query(Payment).filter(
            (Payment.from_user_id == user_id) | (Payment.to_user_id == user_id)
        ).all() 