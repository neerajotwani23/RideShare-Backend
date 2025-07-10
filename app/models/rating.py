from sqlalchemy import Column, Integer, Text, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from .base import Base

class RatingsReviews(Base):
    __tablename__ = "ratings_reviews"
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    reviewer_id = Column(Integer, ForeignKey("users.id"), nullable=False)  # User giving the review
    reviewee_id = Column(Integer, ForeignKey("users.id"), nullable=False)  # User receiving the review
    stars = Column(Integer, nullable=False)  # 1-5 rating
    text_review = Column(Text, nullable=True)
    created_at = Column(DateTime, default=func.now())
    
    # Relationships
    reviewer = relationship("User", foreign_keys=[reviewer_id], back_populates="reviews_given")
    reviewee = relationship("User", foreign_keys=[reviewee_id], back_populates="reviews_received") 