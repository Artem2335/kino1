from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel
from typing import Optional
from app import db

router = APIRouter(tags=["reviews"])


class ReviewCreate(BaseModel):
    text: str
    rating: Optional[int] = None


class ReviewUpdate(BaseModel):
    text: Optional[str] = None
    rating: Optional[int] = None


# Nested routes under movies
@router.get("/api/movies/{movie_id}/reviews", operation_id="get_reviews_by_movie")
def get_movie_reviews(movie_id: int, approved_only: bool = Query(False)):
    """Get reviews for a specific movie"""
    # Check if movie exists
    movie = db.get_movie_by_id(movie_id)
    if not movie:
        raise HTTPException(status_code=404, detail="Movie not found")
    
    reviews = db.get_movie_reviews(movie_id, approved_only=approved_only)
    return reviews


@router.post("/api/movies/{movie_id}/reviews", operation_id="create_movie_review")
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


# Direct review routes
@router.get("/api/reviews/{review_id}", operation_id="get_review_by_id")
def get_review(review_id: int):
    """Get a specific review by ID"""
    review = db.get_review_by_id(review_id)
    if not review:
        raise HTTPException(status_code=404, detail="Review not found")
    return review


@router.put("/api/reviews/{review_id}", operation_id="update_review_by_id")
def update_review(review_id: int, data: ReviewUpdate, user_id: int = None):
    """Update a review (only by author)"""
    review = db.get_review_by_id(review_id)
    if not review:
        raise HTTPException(status_code=404, detail="Review not found")
    
    # Check if user is the author (skip if user_id not provided)
    if user_id and review['user_id'] != user_id:
        raise HTTPException(status_code=403, detail="Not authorized to update this review")
    
    # Update review
    db.update_review(review_id, data.text, data.rating)
    return db.get_review_by_id(review_id)


@router.delete("/api/reviews/{review_id}", operation_id="delete_review_by_id")
def delete_review(review_id: int, user_id: int = None):
    """Delete a review (author or admin)"""
    review = db.get_review_by_id(review_id)
    if not review:
        raise HTTPException(status_code=404, detail="Review not found")
    
    # Check if user is the author (skip if user_id not provided)
    if user_id and review['user_id'] != user_id:
        raise HTTPException(status_code=403, detail="Not authorized to delete this review")
    
    db.delete_review(review_id)
    return {"status": "deleted"}


@router.put("/api/reviews/{review_id}/approve", operation_id="approve_review_by_id")
def approve_review(review_id: int):
    """Approve a review (moderator only)"""
    review = db.get_review_by_id(review_id)
    if not review:
        raise HTTPException(status_code=404, detail="Review not found")
    
    db.approve_review(review_id)
    return {"status": "approved"}
