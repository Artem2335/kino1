"""Initialize SQLite database for v2.0.0

Note: This script creates the database schema WITHOUT the ratings table.
Ratings functionality has been moved to review ratings.
Use this for fresh installations only.

For existing installations, use Alembic migration:
    cd app
    alembic upgrade head
"""
import sqlite3
import os
from pathlib import Path
from app.db import hash_password

DB_PATH = Path(__file__).parent / "kinovzor.db"

def init_db():
    """Create all tables for v2.0.0
    
    Tables created:
    - users (with password hashing support)
    - movies
    - reviews (with optional rating field)
    - favorites
    
    Removed tables:
    - ratings (functionality moved to review ratings)
    """
    
    # Remove old db if exists
    if DB_PATH.exists():
        os.remove(DB_PATH)
        print("🗑️  Old database removed")
    
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    print("\n📊 Creating database tables for v2.0.0...\n")
    
    # Users table
    print("  ✓ Creating users table...")
    cursor.execute("""
    CREATE TABLE users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        email TEXT UNIQUE NOT NULL,
        password TEXT NOT NULL,
        username TEXT NOT NULL,
        is_user BOOLEAN DEFAULT 1,
        is_moderator BOOLEAN DEFAULT 0,
        is_admin BOOLEAN DEFAULT 0,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)
    
    # Movies table
    print("  ✓ Creating movies table...")
    cursor.execute("""
    CREATE TABLE movies (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        description TEXT,
        genre TEXT NOT NULL,
        year INTEGER NOT NULL,
        poster_url TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)
    
    # Reviews table - with optional rating field
    print("  ✓ Creating reviews table...")
    cursor.execute("""
    CREATE TABLE reviews (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        movie_id INTEGER NOT NULL,
        user_id INTEGER NOT NULL,
        text TEXT NOT NULL,
        rating INTEGER,
        approved BOOLEAN DEFAULT 0,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (movie_id) REFERENCES movies(id),
        FOREIGN KEY (user_id) REFERENCES users(id)
    )
    """)
    
    # Favorites table
    print("  ✓ Creating favorites table...")
    cursor.execute("""
    CREATE TABLE favorites (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        movie_id INTEGER NOT NULL,
        user_id INTEGER NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (movie_id) REFERENCES movies(id),
        FOREIGN KEY (user_id) REFERENCES users(id)
    )
    """)
    
    conn.commit()
    conn.close()
    
    # Print summary
    print("\n" + "="*50)
    print("✅ Database initialized successfully!")
    print("="*50)
    print(f"📁 Database: {DB_PATH}")
    print(f"📋 Tables created:")
    print(f"   • users (with password hashing)")
    print(f"   • movies")
    print(f"   • reviews (with optional rating)")
    print(f"   • favorites")
    print(f"\n🗑️  Removed from v2.0.0:")
    print(f"   • ratings table (use review ratings)")
    print(f"\n💾 Version: 2.0.0")
    print(f"🔐 Passwords: Automatically hashed with bcrypt")
    print(f"\n📚 Next steps:")
    print(f"   1. Run: python run.py")
    print(f"   2. Server will seed sample data automatically")
    print(f"   3. Access: http://localhost:8000/static/index.html")
    print("="*50 + "\n")

if __name__ == "__main__":
    init_db()
