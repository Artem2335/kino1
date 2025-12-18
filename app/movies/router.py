from fastapi import APIRouter, HTTPException, Query, Depends, Request
from pydantic import BaseModel
from typing import Optional, List
from app import db
import jwt
from datetime import datetime

router = APIRouter(prefix="/api/movies", tags=["movies"])

class MovieCreate(BaseModel):
    title: str
    description: Optional[str] = None
    genre: str
    year: int
    poster_url: Optional[str] = None


class MovieUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    genre: Optional[str] = None
    year: Optional[int] = None
    poster_url: Optional[str] = None


class ReviewCreate(BaseModel):
    text: str
    rating: Optional[int] = None


def get_current_user(request: Request):
    """Extract user from JWT token in cookies"""
    token = request.cookies.get("access_token")
    if not token:
        raise HTTPException(status_code=401, detail="Not authenticated")
    
    try:
        payload = jwt.decode(token, "your-secret-key", algorithms=["HS256"])
        user_id = payload.get("user_id")
        if user_id is None:
            raise HTTPException(status_code=401, detail="Invalid token")
        return user_id
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token")


# ========== MOVIES ==========

@router.get("/")
def get_movies(genre: Optional[str] = Query(None), sort: str = Query("popular")):
    """Get all movies with optional filtering and sorting"""
    movies = db.get_all_movies()
    
    if genre and genre != "all":
        movies = [m for m in movies if m['genre'] == genre]
    
    if sort == "title":
        movies = sorted(movies, key=lambda x: x['title'])
    elif sort == "year":
        movies = sorted(movies, key=lambda x: x['year'], reverse=True)
    # Default is popular (by id desc, already done)
    
    return movies

@router.get("/stats")
def get_stats():
    """Get overall site statistics"""
    movies = db.get_all_movies()
    movies_count = len(movies)
    
    # Count all reviews
    reviews_count = 0
    for movie in movies:
        reviews = db.get_movie_reviews(movie['id'], approved_only=False)
        reviews_count += len(reviews)
    
    return {
        "movies_count": movies_count,
        "reviews_count": reviews_count
    }

@router.get("/{movie_id}")
def get_movie(movie_id: int):
    """Get a single movie by ID"""
    movie = db.get_movie_by_id(movie_id)
    
    if not movie:
        raise HTTPException(status_code=404, detail="Movie not found")
    
    return movie

@router.post("/")
def create_movie(data: MovieCreate):
    """Create a new movie (admin only)"""
    movie = db.create_movie(
        title=data.title,
        description=data.description,
        genre=data.genre,
        year=data.year,
        poster_url=data.poster_url
    )
    return movie

@router.put("/{movie_id}")
def update_movie(movie_id: int, data: MovieUpdate):
    """Update a movie (admin only)"""
    movie = db.get_movie_by_id(movie_id)
    if not movie:
        raise HTTPException(status_code=404, detail="Movie not found")
    
    db.update_movie(
        movie_id=movie_id,
        title=data.title,
        description=data.description,
        genre=data.genre,
        year=data.year,
        poster_url=data.poster_url
    )
    return db.get_movie_by_id(movie_id)

@router.delete("/{movie_id}")
def delete_movie(movie_id: int):
    """Delete a movie (admin only)"""
    movie = db.get_movie_by_id(movie_id)
    if not movie:
        raise HTTPException(status_code=404, detail="Movie not found")
    
    db.delete_movie(movie_id)
    return {"status": "deleted"}


# ========== REVIEWS FOR MOVIES ==========

@router.get("/{movie_id}/reviews")
def get_movie_reviews(movie_id: int, approved_only: bool = Query(True)):
    """Get reviews for a specific movie"""
    movie = db.get_movie_by_id(movie_id)
    if not movie:
        raise HTTPException(status_code=404, detail="Movie not found")
    
    reviews = db.get_movie_reviews(movie_id, approved_only=approved_only)
    return reviews


@router.post("/{movie_id}/reviews")
def create_movie_review(movie_id: int, data: ReviewCreate, request: Request):
    """Create a review for a specific movie"""
    movie = db.get_movie_by_id(movie_id)
    if not movie:
        raise HTTPException(status_code=404, detail="Movie not found")
    
    # Get user from JWT token
    user_id = get_current_user(request)
    
    review = db.create_review(
        movie_id=movie_id,
        user_id=user_id,
        text=data.text,
        rating=data.rating
    )
    return review


@router.delete("/reviews/{review_id}")
def delete_movie_review(review_id: int, request: Request):
    """Delete a review (author or admin)"""
    # Get user from JWT token
    user_id = get_current_user(request)
    
    review = db.get_review_by_id(review_id)
    if not review:
        raise HTTPException(status_code=404, detail="Review not found")
    
    # Check if user is the author or admin
    if review['user_id'] != user_id:
        raise HTTPException(status_code=403, detail="Not authorized to delete this review")
    
    db.delete_review(review_id)
    return {"status": "deleted"}


# ========== RATING STATS FOR MOVIES ==========

@router.get("/{movie_id}/rating-stats")
def get_movie_rating_stats(movie_id: int):
    """Get rating statistics for a specific movie"""
    movie = db.get_movie_by_id(movie_id)
    if not movie:
        raise HTTPException(status_code=404, detail="Movie not found")
    
    stats = db.get_rating_stats(movie_id)
    return stats


# ========== FAVORITES FOR MOVIES ==========

@router.post("/{movie_id}/favorites")
def add_movie_to_favorites(movie_id: int, request: Request):
    """Add a movie to user's favorites"""
    movie = db.get_movie_by_id(movie_id)
    if not movie:
        raise HTTPException(status_code=404, detail="Movie not found")
    
    # Get user from JWT token
    user_id = get_current_user(request)
    
    result = db.add_favorite(movie_id, user_id)
    
    if "error" in result:
        raise HTTPException(status_code=400, detail=result["error"])
    
    return result


@router.delete("/{movie_id}/favorites")
def remove_movie_from_favorites(movie_id: int, request: Request):
    """Remove a movie from user's favorites"""
    movie = db.get_movie_by_id(movie_id)
    if not movie:
        raise HTTPException(status_code=404, detail="Movie not found")
    
    # Get user from JWT token
    user_id = get_current_user(request)
    
    result = db.remove_favorite(movie_id, user_id)
    return result


@router.get("/user/{user_id}/favorites")
def get_user_favorites(user_id: int):
    """Get user's favorite movies"""
    favorites = db.get_user_favorites(user_id)
    return favorites
