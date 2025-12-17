from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel
from typing import Optional
from app import db

router = APIRouter(prefix="/api/reviews", tags=["reviews"])


class ReviewCreate(BaseModel):
    text: str
    rating: Optional[int] = None


class ReviewUpdate(BaseModel):
    text: Optional[str] = None
    rating: Optional[int] = None


@router.post("/")
def create_review(movie_id: int, user_id: int, data: ReviewCreate):
    """Create a review for a movie"""
    # Check if movie exists
    movie = db.get_movie_by_id(movie_id)
    if not movie:
        raise HTTPException(status_code=404, detail="Movie not found")
    
    review = db.create_review(
        movie_id=movie_id,
        user_id=user_id,
        text=data.text,
        rating=data.rating
    )
    return review


@router.get("/movies/{movie_id}")
def get_reviews(movie_id: int, approved_only: bool = Query(True)):
    """Get reviews for a movie"""
    reviews = db.get_movie_reviews(movie_id, approved_only=approved_only)
    return reviews


@router.get("/{review_id}")
def get_review(review_id: int):
    """Get a specific review by ID"""
    review = db.get_review_by_id(review_id)
    if not review:
        raise HTTPException(status_code=404, detail="Review not found")
    return review


@router.put("/{review_id}")
def update_review(review_id: int, data: ReviewUpdate, user_id: int):
    """Update a review (only by author)"""
    review = db.get_review_by_id(review_id)
    if not review:
        raise HTTPException(status_code=404, detail="Review not found")
    
    # Check if user is the author
    if review['user_id'] != user_id:
        raise HTTPException(status_code=403, detail="Not authorized to update this review")
    
    # Update review
    db.update_review(review_id, data.text, data.rating)
    return db.get_review_by_id(review_id)


@router.delete("/{review_id}")
def delete_review(review_id: int, user_id: int):
    """Delete a review (author or admin)"""
    review = db.get_review_by_id(review_id)
    if not review:
        raise HTTPException(status_code=404, detail="Review not found")
    
    # Check if user is the author
    if review['user_id'] != user_id:
        raise HTTPException(status_code=403, detail="Not authorized to delete this review")
    
    db.delete_review(review_id)
    return {"status": "deleted"}


@router.put("/{review_id}/approve")
def approve_review(review_id: int):
    """Approve a review (moderator only)"""
    review = db.get_review_by_id(review_id)
    if not review:
        raise HTTPException(status_code=404, detail="Review not found")
    
    db.approve_review(review_id)
    return {"status": "approved"}
