from fastapi import APIRouter, HTTPException
from app import db

router = APIRouter(prefix="/api/favorites", tags=["favorites"])


@router.post("/")
def add_to_favorites(movie_id: int, user_id: int):
    """Add a movie to favorites"""
    # Check if movie exists
    movie = db.get_movie_by_id(movie_id)
    if not movie:
        raise HTTPException(status_code=404, detail="Movie not found")
    
    result = db.add_favorite(movie_id, user_id)
    
    if "error" in result:
        raise HTTPException(status_code=400, detail=result["error"])
    
    return result


@router.delete("/")
def remove_from_favorites(movie_id: int, user_id: int):
    """Remove a movie from favorites"""
    result = db.remove_favorite(movie_id, user_id)
    return result


@router.get("/")
def get_user_favorites(user_id: int):
    """Get user's favorite movies"""
    favorites = db.get_user_favorites(user_id)
    return favorites


@router.get("/check/{movie_id}")
def is_favorite(movie_id: int, user_id: int):
    """Check if a movie is in user's favorites"""
    is_fav = db.is_favorite(movie_id, user_id)
    return {"is_favorite": is_fav}
