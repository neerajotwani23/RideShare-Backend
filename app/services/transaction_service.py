from sqlalchemy.orm import Session
from typing import List

from ..repositories import TransactionRepository
from ..models import Transaction
from .. import schemas

class TransactionService:
    def __init__(self, db: Session):
        self.db = db
        self.transaction_repo = TransactionRepository(db)
    
    def create_transaction(self, transaction: schemas.TransactionCreate) -> Transaction:
        """Create a new transaction with wallet updates"""
        return self.transaction_repo.create(transaction)
    
    def get_user_transactions(self, user_id: int, skip: int = 0, limit: int = 10) -> List[Transaction]:
        """Get user transaction history"""
        return self.transaction_repo.get_by_user_id(user_id, skip, limit) 