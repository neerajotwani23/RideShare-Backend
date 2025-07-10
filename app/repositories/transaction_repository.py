from sqlalchemy.orm import Session
from typing import List
from fastapi import HTTPException

from ..models import Transaction, User
from .. import schemas

class TransactionRepository:
    def __init__(self, db: Session):
        self.db = db
    
    def create(self, transaction: schemas.TransactionCreate) -> Transaction:
        # Check if user exists
        user = self.db.query(User).filter(User.id == transaction.user_id).first()
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        
        # Create transaction
        db_transaction = Transaction(**transaction.dict())
        self.db.add(db_transaction)
        
        # Update user wallet based on transaction type
        if transaction.type.value == "debit":
            if user.wallet < transaction.amount:
                raise HTTPException(status_code=400, detail="Insufficient wallet balance")
            user.wallet -= transaction.amount
        else:  # credit
            user.wallet += transaction.amount
        
        self.db.commit()
        self.db.refresh(db_transaction)
        return db_transaction
    
    def get_by_user_id(self, user_id: int, skip: int = 0, limit: int = 10) -> List[Transaction]:
        return self.db.query(Transaction).filter(
            Transaction.user_id == user_id
        ).order_by(Transaction.datetime.desc()).offset(skip).limit(limit).all() 