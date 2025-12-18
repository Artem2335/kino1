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


class ReviewCreate(BaseModel):
    text: str
    rating: Optional[int] = None


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
def create_movie_review(movie_id: int, user_id: int, data: ReviewCreate):
    """Create a review for a specific movie"""
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
def add_movie_to_favorites(movie_id: int, user_id: int):
    """Add a movie to user's favorites"""
    movie = db.get_movie_by_id(movie_id)
    if not movie:
        raise HTTPException(status_code=404, detail="Movie not found")
    
    result = db.add_favorite(movie_id, user_id)
    
    if "error" in result:
        raise HTTPException(status_code=400, detail=result["error"])
    
    return result


@router.delete("/{movie_id}/favorites")
def remove_movie_from_favorites(movie_id: int, user_id: int):
    """Remove a movie from user's favorites"""
    movie = db.get_movie_by_id(movie_id)
    if not movie:
        raise HTTPException(status_code=404, detail="Movie not found")
    
    result = db.remove_favorite(movie_id, user_id)
    return result


@router.get("/user/{user_id}/favorites")
def get_user_favorites(user_id: int):
    """Get user's favorite movies"""
    favorites = db.get_user_favorites(user_id)
    return favorites
