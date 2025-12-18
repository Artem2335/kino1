"""Database helper functions using sqlite3"""
import sqlite3
from pathlib import Path
from typing import Any, Dict, List, Optional
import json
from datetime import datetime

DB_PATH = Path(__file__).parent.parent / "kinovzor.db"

def get_db() -> sqlite3.Connection:
    """Get database connection with timeout and other optimizations"""
    conn = sqlite3.connect(DB_PATH, timeout=30.0, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    # Enable WAL mode for better concurrency
    try:
        conn.execute("PRAGMA journal_mode=WAL")
    except:
        pass
    # Set synchronous to NORMAL for better performance
    try:
        conn.execute("PRAGMA synchronous=NORMAL")
    except:
        pass
    return conn

def dict_from_row(row: sqlite3.Row) -> Dict[str, Any]:
    """Convert sqlite3.Row to dict"""
    if row is None:
        return None
    return dict(row)

def dicts_from_rows(rows: List[sqlite3.Row]) -> List[Dict[str, Any]]:
    """Convert list of sqlite3.Row to list of dicts"""
    return [dict(row) for row in rows]

# Users
def get_user_by_email(email: str) -> Optional[Dict]:
    conn = get_db()
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE email = ?", (email,))
        user = cursor.fetchone()
        return dict_from_row(user)
    finally:
        conn.close()

def get_user_by_username(username: str) -> Optional[Dict]:
    """Get user by username"""
    conn = get_db()
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
        user = cursor.fetchone()
        return dict_from_row(user)
    finally:
        conn.close()

def get_user_by_id(user_id: int) -> Optional[Dict]:
    conn = get_db()
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE id = ?", (user_id,))
        user = cursor.fetchone()
        return dict_from_row(user)
    finally:
        conn.close()

def create_user(email: str, password: str, username: str, is_moderator: bool = False) -> Dict:
    """Create user with optional moderator flag"""
    conn = get_db()
    try:
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO users (email, password, username, is_moderator) VALUES (?, ?, ?, ?)",
            (email, password, username, is_moderator)
        )
        conn.commit()
        user_id = cursor.lastrowid
        return get_user_by_id(user_id)
    finally:
        conn.close()

def update_user(user_id: int, email: str = None, username: str = None, password: str = None) -> Dict:
    """Update user profile"""
    conn = get_db()
    try:
        cursor = conn.cursor()
        
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
            params.append(password)
        
        if updates:
            params.append(user_id)
            query = f"UPDATE users SET {', '.join(updates)} WHERE id = ?"
            cursor.execute(query, params)
            conn.commit()
        
        return get_user_by_id(user_id)
    finally:
        conn.close()

def delete_user(user_id: int) -> bool:
    """Delete user and associated data"""
    conn = get_db()
    try:
        cursor = conn.cursor()
        
        # Delete favorites
        cursor.execute("DELETE FROM favorites WHERE user_id = ?", (user_id,))
        # Delete reviews
        cursor.execute("DELETE FROM reviews WHERE user_id = ?", (user_id,))
        # Delete ratings
        cursor.execute("DELETE FROM ratings WHERE user_id = ?", (user_id,))
        # Delete user
        cursor.execute("DELETE FROM users WHERE id = ?", (user_id,))
        
        conn.commit()
        return True
    finally:
        conn.close()

# Movies
def get_all_movies() -> List[Dict]:
    conn = get_db()
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM movies ORDER BY id DESC")
        movies = cursor.fetchall()
        return dicts_from_rows(movies)
    finally:
        conn.close()

def get_movie_by_id(movie_id: int) -> Optional[Dict]:
    conn = get_db()
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM movies WHERE id = ?", (movie_id,))
        movie = cursor.fetchone()
        return dict_from_row(movie)
    finally:
        conn.close()

def create_movie(title: str, description: str, genre: str, year: int, poster_url: str = None) -> Dict:
    conn = get_db()
    try:
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO movies (title, description, genre, year, poster_url) VALUES (?, ?, ?, ?, ?)",
            (title, description, genre, year, poster_url)
        )
        conn.commit()
        movie_id = cursor.lastrowid
        return get_movie_by_id(movie_id)
    finally:
        conn.close()

def update_movie(movie_id: int, title: str = None, description: str = None, genre: str = None, year: int = None, poster_url: str = None) -> Dict:
    """Update movie information"""
    conn = get_db()
    try:
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
        
        if updates:
            params.append(movie_id)
            query = f"UPDATE movies SET {', '.join(updates)} WHERE id = ?"
            cursor.execute(query, params)
            conn.commit()
        
        return get_movie_by_id(movie_id)
    finally:
        conn.close()

def delete_movie(movie_id: int) -> bool:
    """Delete movie and associated data"""
    conn = get_db()
    try:
        cursor = conn.cursor()
        
        # Delete favorites
        cursor.execute("DELETE FROM favorites WHERE movie_id = ?", (movie_id,))
        # Delete reviews
        cursor.execute("DELETE FROM reviews WHERE movie_id = ?", (movie_id,))
        # Delete ratings
        cursor.execute("DELETE FROM ratings WHERE movie_id = ?", (movie_id,))
        # Delete movie
        cursor.execute("DELETE FROM movies WHERE id = ?", (movie_id,))
        
        conn.commit()
        return True
    finally:
        conn.close()

# Reviews
def create_review(movie_id: int, user_id: int, text: str, rating: int = None) -> Dict:
    conn = get_db()
    try:
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO reviews (movie_id, user_id, text, rating, approved) VALUES (?, ?, ?, ?, ?)",
            (movie_id, user_id, text, rating, False)
        )
        conn.commit()
        review_id = cursor.lastrowid
        return get_review_by_id(review_id)
    finally:
        conn.close()

def get_review_by_id(review_id: int) -> Optional[Dict]:
    conn = get_db()
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT r.*, u.username FROM reviews r LEFT JOIN users u ON r.user_id = u.id WHERE r.id = ?", (review_id,))
        review = cursor.fetchone()
        return dict_from_row(review)
    finally:
        conn.close()

def get_movie_reviews(movie_id: int, approved_only: bool = True) -> List[Dict]:
    conn = get_db()
    try:
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
        return dicts_from_rows(reviews)
    finally:
        conn.close()

def update_review(review_id: int, text: str = None, rating: int = None) -> Dict:
    """Update review information"""
    conn = get_db()
    try:
        cursor = conn.cursor()
        
        updates = []
        params = []
        
        if text is not None:
            updates.append("text = ?")
            params.append(text)
        if rating is not None:
            updates.append("rating = ?")
            params.append(rating)
        
        if updates:
            params.append(review_id)
            query = f"UPDATE reviews SET {', '.join(updates)} WHERE id = ?"
            cursor.execute(query, params)
            conn.commit()
        
        return get_review_by_id(review_id)
    finally:
        conn.close()

def approve_review(review_id: int) -> bool:
    conn = get_db()
    try:
        cursor = conn.cursor()
        cursor.execute("UPDATE reviews SET approved = 1 WHERE id = ?", (review_id,))
        conn.commit()
        return True
    finally:
        conn.close()

def delete_review(review_id: int) -> bool:
    conn = get_db()
    try:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM reviews WHERE id = ?", (review_id,))
        conn.commit()
        return True
    finally:
        conn.close()

# Ratings - Calculate from reviews
def get_rating_stats(movie_id: int) -> Dict:
    """Получаем статистику рейтинга из оценок рецензий"""
    conn = get_db()
    try:
        cursor = conn.cursor()
        # считаем средние и количество оценок из рецензий
        cursor.execute(
            "SELECT COUNT(*) as count, AVG(rating) as average FROM reviews WHERE movie_id = ? AND rating IS NOT NULL",
            (movie_id,)
        )
        result = cursor.fetchone()
        
        if result and result['count'] > 0:
            return {
                "count": result['count'],
                "average": round(float(result['average']), 1)
            }
        return {"count": 0, "average": None}
    finally:
        conn.close()

def create_or_update_rating(movie_id: int, user_id: int, value: float) -> Dict:
    """Legacy function - kept for compatibility"""
    conn = get_db()
    try:
        cursor = conn.cursor()
        
        # Check if rating exists
        cursor.execute("SELECT * FROM ratings WHERE movie_id = ? AND user_id = ?", (movie_id, user_id))
        existing = cursor.fetchone()
        
        if existing:
            cursor.execute("UPDATE ratings SET value = ? WHERE movie_id = ? AND user_id = ?", (value, movie_id, user_id))
            rating_id = existing['id']
        else:
            cursor.execute(
                "INSERT INTO ratings (movie_id, user_id, value) VALUES (?, ?, ?)",
                (movie_id, user_id, value)
            )
            rating_id = cursor.lastrowid
        
        conn.commit()
        return get_rating_by_id(rating_id)
    finally:
        conn.close()

def get_rating_by_id(rating_id: int) -> Optional[Dict]:
    conn = get_db()
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM ratings WHERE id = ?", (rating_id,))
        rating = cursor.fetchone()
        return dict_from_row(rating)
    finally:
        conn.close()

def get_movie_ratings(movie_id: int) -> List[Dict]:
    conn = get_db()
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM ratings WHERE movie_id = ?", (movie_id,))
        ratings = cursor.fetchall()
        return dicts_from_rows(ratings)
    finally:
        conn.close()

# Favorites
def add_favorite(movie_id: int, user_id: int) -> Dict:
    conn = get_db()
    try:
        cursor = conn.cursor()
        
        # Check if already exists
        cursor.execute("SELECT * FROM favorites WHERE movie_id = ? AND user_id = ?", (movie_id, user_id))
        if cursor.fetchone():
            return {"error": "Already in favorites"}
        
        cursor.execute(
            "INSERT INTO favorites (movie_id, user_id) VALUES (?, ?)",
            (movie_id, user_id)
        )
        conn.commit()
        return {"status": "added"}
    finally:
        conn.close()

def remove_favorite(movie_id: int, user_id: int) -> Dict:
    conn = get_db()
    try:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM favorites WHERE movie_id = ? AND user_id = ?", (movie_id, user_id))
        conn.commit()
        return {"status": "removed"}
    finally:
        conn.close()

def get_user_favorites(user_id: int) -> List[Dict]:
    conn = get_db()
    try:
        cursor = conn.cursor()
        cursor.execute(
            "SELECT m.* FROM movies m JOIN favorites f ON m.id = f.movie_id WHERE f.user_id = ?",
            (user_id,)
        )
        movies = cursor.fetchall()
        return dicts_from_rows(movies)
    finally:
        conn.close()

def is_favorite(movie_id: int, user_id: int) -> bool:
    conn = get_db()
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT 1 FROM favorites WHERE movie_id = ? AND user_id = ?", (movie_id, user_id))
        result = cursor.fetchone()
        return result is not None
    finally:
        conn.close()
