from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from typing import List

from ..services import TransactionService
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

class TransactionController:
    def __init__(self):
        self.router = APIRouter(prefix="/transactions", tags=["Transactions"])
        self._setup_routes()
    
    def _setup_routes(self):
        self.router.add_api_route("/", self.create_transaction, methods=["POST"], response_model=schemas.TransactionResponse)
        self.router.add_api_route("/my-transactions", self.get_my_transactions, methods=["GET"], response_model=List[schemas.TransactionResponse])
    
    def create_transaction(
        self,
        transaction: schemas.TransactionCreate,
        current_user: User = Depends(AuthController.get_current_user),
        db: Session = Depends(get_db)
    ):
        """Create a new transaction"""
        transaction_service = TransactionService(db)
        transaction.user_id = current_user.id
        return transaction_service.create_transaction(transaction)
    
    def get_my_transactions(
        self,
        skip: int = Query(0, description="Number of records to skip"),
        limit: int = Query(10, description="Number of records to return"),
        current_user: User = Depends(AuthController.get_current_user),
        db: Session = Depends(get_db)
    ):
        """Get current user's transaction history"""
        transaction_service = TransactionService(db)
        return transaction_service.get_user_transactions(current_user.id, skip, limit) 