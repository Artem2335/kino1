from fastapi import APIRouter, HTTPException, Request
from app import db

router = APIRouter(prefix="/api/favorites", tags=["favorites"])


@router.post("/{movie_id}")
def add_to_favorites(movie_id: int, request: Request):
    """Add a movie to favorites"""
    # Get user from JWT token
    try:
        import jwt
        token = request.cookies.get("access_token")
        if not token:
            raise HTTPException(status_code=401, detail="Not authenticated")
        payload = jwt.decode(token, "your-secret-key", algorithms=["HS256"])
        user_id = payload.get("user_id")
        if user_id is None:
            raise HTTPException(status_code=401, detail="Invalid token")
    except Exception as e:
        raise HTTPException(status_code=401, detail="Authentication failed")
    
    # Check if movie exists
    movie = db.get_movie_by_id(movie_id)
    if not movie:
        raise HTTPException(status_code=404, detail="Movie not found")
    
    result = db.add_favorite(movie_id, user_id)
    
    if "error" in result:
        raise HTTPException(status_code=400, detail=result["error"])
    
    return result


@router.delete("/{movie_id}")
def remove_from_favorites(movie_id: int, request: Request):
    """Remove a movie from favorites"""
    # Get user from JWT token
    try:
        import jwt
        token = request.cookies.get("access_token")
        if not token:
            raise HTTPException(status_code=401, detail="Not authenticated")
        payload = jwt.decode(token, "your-secret-key", algorithms=["HS256"])
        user_id = payload.get("user_id")
        if user_id is None:
            raise HTTPException(status_code=401, detail="Invalid token")
    except Exception as e:
        raise HTTPException(status_code=401, detail="Authentication failed")
    
    result = db.remove_favorite(movie_id, user_id)
    return result


@router.get("/")
def get_user_favorites(request: Request):
    """Get user's favorite movies"""
    # Get user from JWT token
    try:
        import jwt
        token = request.cookies.get("access_token")
        if not token:
            raise HTTPException(status_code=401, detail="Not authenticated")
        payload = jwt.decode(token, "your-secret-key", algorithms=["HS256"])
        user_id = payload.get("user_id")
        if user_id is None:
            raise HTTPException(status_code=401, detail="Invalid token")
    except Exception as e:
        raise HTTPException(status_code=401, detail="Authentication failed")
    
    favorites = db.get_user_favorites(user_id)
    return favorites


@router.get("/check/{movie_id}")
def is_favorite(movie_id: int, request: Request):
    """Check if a movie is in user's favorites"""
    # Get user from JWT token
    try:
        import jwt
        token = request.cookies.get("access_token")
        if not token:
            raise HTTPException(status_code=401, detail="Not authenticated")
        payload = jwt.decode(token, "your-secret-key", algorithms=["HS256"])
        user_id = payload.get("user_id")
        if user_id is None:
            raise HTTPException(status_code=401, detail="Invalid token")
    except Exception as e:
        raise HTTPException(status_code=401, detail="Authentication failed")
    
    is_fav = db.is_favorite(movie_id, user_id)
    return {"is_favorite": is_fav}
