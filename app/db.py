"""Database helper functions using sqlite3"""
import sqlite3
from pathlib import Path
from typing import Any, Dict, List, Optional
import json
from datetime import datetime
from passlib.context import CryptContext

DB_PATH = Path(__file__).parent.parent / "kinovzor.db"

# Password hashing context
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_db() -> sqlite3.Connection:
    """Get database connection"""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def dict_from_row(row: sqlite3.Row) -> Dict[str, Any]:
    """Convert sqlite3.Row to dict"""
    if row is None:
        return None
    return dict(row)

def dicts_from_rows(rows: List[sqlite3.Row]) -> List[Dict[str, Any]]:
    """Convert list of sqlite3.Row to list of dicts"""
    return [dict(row) for row in rows]

def hash_password(password: str) -> str:
    """Hash a password using bcrypt"""
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a password against its hash"""
    return pwd_context.verify(plain_password, hashed_password)

# ========== USERS ==========

def get_user_by_email(email: str) -> Optional[Dict]:
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE email = ?", (email,))
    user = cursor.fetchone()
    conn.close()
    return dict_from_row(user)

def get_user_by_username(username: str) -> Optional[Dict]:
    """Get user by username"""
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
    user = cursor.fetchone()
    conn.close()
    return dict_from_row(user)

def get_user_by_id(user_id: int) -> Optional[Dict]:
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE id = ?", (user_id,))
    user = cursor.fetchone()
    conn.close()
    return dict_from_row(user)

def create_user(email: str, password: str, username: str, is_moderator: bool = False) -> Dict:
    """Create user with hashed password and optional moderator flag"""
    conn = get_db()
    cursor = conn.cursor()
    hashed_pwd = hash_password(password)
    cursor.execute(
        "INSERT INTO users (email, password, username, is_moderator) VALUES (?, ?, ?, ?)",
        (email, hashed_pwd, username, is_moderator)
    )
    conn.commit()
    user_id = cursor.lastrowid
    conn.close()
    return get_user_by_id(user_id)

def update_user(user_id: int, email: str = None, username: str = None, password: str = None) -> Dict:
    """Update user profile (password will be hashed if provided)"""
    conn = get_db()
    cursor = conn.cursor()
    
    # Build dynamic update query
    updates = []
    params = []
    
    if email is not None:
        updates.append("email = ?")
        params.append(email)
    if username is not None:
        updates.append("username = ?")
        params.append(username)
    if password is not None:
        updates.append("password = ?")
        params.append(hash_password(password))
    
    if not updates:
        conn.close()
        return get_user_by_id(user_id)
    
    params.append(user_id)
    query = f"UPDATE users SET {', '.join(updates)} WHERE id = ?"
    cursor.execute(query, params)
    conn.commit()
    conn.close()
    return get_user_by_id(user_id)

def delete_user(user_id: int) -> bool:
    """Delete user and all related data"""
    conn = get_db()
    cursor = conn.cursor()
    
    # Delete user's reviews first
    cursor.execute("DELETE FROM reviews WHERE user_id = ?", (user_id,))
    # Delete user's favorites
    cursor.execute("DELETE FROM favorites WHERE user_id = ?", (user_id,))
    # Delete user
    cursor.execute("DELETE FROM users WHERE id = ?", (user_id,))
    
    conn.commit()
    conn.close()
    return True

# ========== MOVIES ==========

def get_all_movies() -> List[Dict]:
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM movies ORDER BY id DESC")
    movies = cursor.fetchall()
    conn.close()
    return dicts_from_rows(movies)

def get_movie_by_id(movie_id: int) -> Optional[Dict]:
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM movies WHERE id = ?", (movie_id,))
    movie = cursor.fetchone()
    conn.close()
    return dict_from_row(movie)

def create_movie(title: str, description: str, genre: str, year: int, poster_url: str = None) -> Dict:
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO movies (title, description, genre, year, poster_url) VALUES (?, ?, ?, ?, ?)",
        (title, description, genre, year, poster_url)
    )
    conn.commit()
    movie_id = cursor.lastrowid
    conn.close()
    return get_movie_by_id(movie_id)

def update_movie(movie_id: int, title: str = None, description: str = None, genre: str = None, year: int = None, poster_url: str = None) -> Dict:
    """Update movie details"""
    conn = get_db()
    cursor = conn.cursor()
    
    updates = []
    params = []
    
    if title is not None:
        updates.append("title = ?")
        params.append(title)
    if description is not None:
        updates.append("description = ?")
        params.append(description)
    if genre is not None:
        updates.append("genre = ?")
        params.append(genre)
    if year is not None:
        updates.append("year = ?")
        params.append(year)
    if poster_url is not None:
        updates.append("poster_url = ?")
        params.append(poster_url)
    
    if not updates:
        conn.close()
        return get_movie_by_id(movie_id)
    
    params.append(movie_id)
    query = f"UPDATE movies SET {', '.join(updates)} WHERE id = ?"
    cursor.execute(query, params)
    conn.commit()
    conn.close()
    return get_movie_by_id(movie_id)

def delete_movie(movie_id: int) -> bool:
    """Delete movie and all related data"""
    conn = get_db()
    cursor = conn.cursor()
    
    # Delete reviews for this movie
    cursor.execute("DELETE FROM reviews WHERE movie_id = ?", (movie_id,))
    # Delete favorites for this movie
    cursor.execute("DELETE FROM favorites WHERE movie_id = ?", (movie_id,))
    # Delete the movie
    cursor.execute("DELETE FROM movies WHERE id = ?", (movie_id,))
    
    conn.commit()
    conn.close()
    return True

# ========== REVIEWS ==========

def create_review(movie_id: int, user_id: int, text: str, rating: int = None) -> Dict:
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO reviews (movie_id, user_id, text, rating, approved) VALUES (?, ?, ?, ?, ?)",
        (movie_id, user_id, text, rating, False)
    )
    conn.commit()
    review_id = cursor.lastrowid
    conn.close()
    return get_review_by_id(review_id)

def get_review_by_id(review_id: int) -> Optional[Dict]:
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT r.*, u.username FROM reviews r LEFT JOIN users u ON r.user_id = u.id WHERE r.id = ?", (review_id,))
    review = cursor.fetchone()
    conn.close()
    return dict_from_row(review)

def get_movie_reviews(movie_id: int, approved_only: bool = True) -> List[Dict]:
    conn = get_db()
    cursor = conn.cursor()
    if approved_only:
        cursor.execute(
            "SELECT r.*, u.username FROM reviews r LEFT JOIN users u ON r.user_id = u.id WHERE r.movie_id = ? AND r.approved = 1 ORDER BY r.created_at DESC", 
            (movie_id,)
        )
    else:
        cursor.execute(
            "SELECT r.*, u.username FROM reviews r LEFT JOIN users u ON r.user_id = u.id WHERE r.movie_id = ? ORDER BY r.created_at DESC", 
            (movie_id,)
        )
    reviews = cursor.fetchall()
    conn.close()
    return dicts_from_rows(reviews)

def update_review(review_id: int, text: str = None, rating: int = None) -> Dict:
    """Update review details"""
    conn = get_db()
    cursor = conn.cursor()
    
    updates = []
    params = []
    
    if text is not None:
        updates.append("text = ?")
        params.append(text)
    if rating is not None:
        updates.append("rating = ?")
        params.append(rating)
    
    if not updates:
        conn.close()
        return get_review_by_id(review_id)
    
    params.append(review_id)
    query = f"UPDATE reviews SET {', '.join(updates)} WHERE id = ?"
    cursor.execute(query, params)
    conn.commit()
    conn.close()
    return get_review_by_id(review_id)

def approve_review(review_id: int) -> bool:
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("UPDATE reviews SET approved = 1 WHERE id = ?", (review_id,))
    conn.commit()
    conn.close()
    return True

def delete_review(review_id: int) -> bool:
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM reviews WHERE id = ?", (review_id,))
    conn.commit()
    conn.close()
    return True

# ========== RATINGS (Removed) ==========
# Ratings functionality has been removed.
# Rating statistics are calculated from review ratings instead.

def get_rating_stats(movie_id: int) -> Dict:
    """Get rating statistics calculated from review ratings"""
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT COUNT(*) as count, AVG(rating) as average FROM reviews WHERE movie_id = ? AND rating IS NOT NULL AND approved = 1",
        (movie_id,)
    )
    result = cursor.fetchone()
    conn.close()
    
    if result and result['count'] > 0:
        return {
            "count": result['count'],
            "average": round(float(result['average']), 1)
        }
    return {"count": 0, "average": None}

# ========== FAVORITES ==========

def add_favorite(movie_id: int, user_id: int) -> Dict:
    conn = get_db()
    cursor = conn.cursor()
    
    # Check if already exists
    cursor.execute("SELECT * FROM favorites WHERE movie_id = ? AND user_id = ?", (movie_id, user_id))
    if cursor.fetchone():
        conn.close()
        return {"error": "Already in favorites"}
    
    cursor.execute(
        "INSERT INTO favorites (movie_id, user_id) VALUES (?, ?)",
        (movie_id, user_id)
    )
    conn.commit()
    conn.close()
    return {"status": "added"}

def remove_favorite(movie_id: int, user_id: int) -> Dict:
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM favorites WHERE movie_id = ? AND user_id = ?", (movie_id, user_id))
    conn.commit()
    conn.close()
    return {"status": "removed"}

def get_user_favorites(user_id: int) -> List[Dict]:
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT m.* FROM movies m JOIN favorites f ON m.id = f.movie_id WHERE f.user_id = ?",
        (user_id,)
    )
    movies = cursor.fetchall()
    conn.close()
    return dicts_from_rows(movies)

def is_favorite(movie_id: int, user_id: int) -> bool:
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT 1 FROM favorites WHERE movie_id = ? AND user_id = ?", (movie_id, user_id))
    result = cursor.fetchone()
    conn.close()
    return result is not None
