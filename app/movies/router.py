from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel
from typing import Optional, List
from app import db

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

@router.get("/{movie_id}/reviews")
def get_movie_reviews(movie_id: int, approved_only: bool = Query(False)):
    """Get reviews for a specific movie"""
    movie = db.get_movie_by_id(movie_id)
    if not movie:
        raise HTTPException(status_code=404, detail="Movie not found")
    
    reviews = db.get_movie_reviews(movie_id, approved_only=approved_only)
    return reviews

@router.post("/{movie_id}/reviews")
def create_movie_review(movie_id: int, user_id: int, text: str, rating: Optional[int] = None):
    """Create a review for a movie (v2.0.0: ratings are part of reviews)"""
    movie = db.get_movie_by_id(movie_id)
    if not movie:
        raise HTTPException(status_code=404, detail="Movie not found")
    
    review_data = {
        "text": text,
        "rating": rating
    }
    
    review = db.create_review(
        movie_id=movie_id,
        user_id=user_id,
        text=text,
        rating=rating
    )
    return review

@router.get("/{movie_id}/rating-stats")
def get_movie_rating_stats(movie_id: int):
    """Get rating statistics for a movie (calculated from review ratings in v2.0.0)"""
    movie = db.get_movie_by_id(movie_id)
    if not movie:
        raise HTTPException(status_code=404, detail="Movie not found")
    
    stats = db.get_rating_stats(movie_id)
    return stats

@router.get("/user/{user_id}/favorites")
def get_user_favorites(user_id: int):
    """Get favorite movies for a specific user"""
    user = db.get_user_by_id(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    favorites = db.get_user_favorites(user_id)
    return favorites

@router.post("/{movie_id}/favorites")
def add_favorite(movie_id: int, user_id: int):
    """Add movie to user's favorites"""
    movie = db.get_movie_by_id(movie_id)
    if not movie:
        raise HTTPException(status_code=404, detail="Movie not found")
    
    user = db.get_user_by_id(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    db.add_favorite(movie_id, user_id)
    return {"status": "added"}

@router.delete("/{movie_id}/favorites")
def remove_favorite(movie_id: int, user_id: int):
    """Remove movie from user's favorites"""
    movie = db.get_movie_by_id(movie_id)
    if not movie:
        raise HTTPException(status_code=404, detail="Movie not found")
    
    user = db.get_user_by_id(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    db.remove_favorite(movie_id, user_id)
    return {"status": "removed"}

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
    
    updated_movie = db.update_movie(
        movie_id=movie_id,
        title=data.title,
        description=data.description,
        genre=data.genre,
        year=data.year,
        poster_url=data.poster_url
    )
    return updated_movie

@router.delete("/{movie_id}")
def delete_movie(movie_id: int):
    """Delete a movie (admin only). Cascades to delete all related reviews and favorites."""
    movie = db.get_movie_by_id(movie_id)
    if not movie:
        raise HTTPException(status_code=404, detail="Movie not found")
    
    db.delete_movie(movie_id)
    return {"status": "deleted"}
