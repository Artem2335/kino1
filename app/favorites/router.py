from fastapi import APIRouter, HTTPException
from app import db

router = APIRouter(tags=["favorites"])


# User favorites - nested under movies
@router.get("/api/movies/user/{user_id}/favorites")
def get_user_favorites(user_id: int):
    """Get all favorite movies for a user"""
    favorites = db.get_user_favorites(user_id)
    return favorites


# Movie favorites - nested under movies
@router.post("/api/movies/{movie_id}/favorites")
def add_to_favorites(movie_id: int, user_id: int):
    """Add a movie to user's favorites"""
    # Check if movie exists
    movie = db.get_movie_by_id(movie_id)
    if not movie:
        raise HTTPException(status_code=404, detail="Movie not found")
    
    result = db.add_favorite(movie_id, user_id)
    
    if "error" in result:
        raise HTTPException(status_code=400, detail=result["error"])
    
    return result


@router.delete("/api/movies/{movie_id}/favorites")
def remove_from_favorites(movie_id: int, user_id: int):
    """Remove a movie from user's favorites"""
    result = db.remove_favorite(movie_id, user_id)
    return result


@router.get("/api/movies/{movie_id}/is-favorite")
def is_favorite(movie_id: int, user_id: int):
    """Check if a movie is in user's favorites"""
    is_fav = db.is_favorite(movie_id, user_id)
    return {"is_favorite": is_fav}


# Alternative direct routes for favorites
@router.get("/api/favorites/{user_id}")
def get_user_favorites_direct(user_id: int):
    """Get all favorite movies for a user (direct route)"""
    favorites = db.get_user_favorites(user_id)
    return favorites


@router.post("/api/favorites/{movie_id}")
def add_to_favorites_direct(movie_id: int, user_id: int):
    """Add a movie to user's favorites (direct route)"""
    # Check if movie exists
    movie = db.get_movie_by_id(movie_id)
    if not movie:
        raise HTTPException(status_code=404, detail="Movie not found")
    
    result = db.add_favorite(movie_id, user_id)
    
    if "error" in result:
        raise HTTPException(status_code=400, detail=result["error"])
    
    return result


@router.delete("/api/favorites/{movie_id}")
def remove_from_favorites_direct(movie_id: int, user_id: int):
    """Remove a movie from user's favorites (direct route)"""
    result = db.remove_favorite(movie_id, user_id)
    return result
