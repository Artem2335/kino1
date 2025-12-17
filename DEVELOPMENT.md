# Development Guide for KinoVzor v2.0.0

This guide covers development setup, testing, and best practices for KinoVzor.

## Development Environment Setup

### Prerequisites

- Python 3.8+
- SQLite3
- Git

### Installation

1. **Clone repository**
```bash
git clone https://github.com/Artem2335/kino1.git
cd kino1
git checkout refactor/crud-operations
```

2. **Create virtual environment**
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Initialize database**
```bash
python run.py  # This will create database and seed data
```

5. **Run server**
```bash
python run.py
# Server runs at http://localhost:8000
```

## Project Structure

```
kino1/
├── app/
│   ├── alembic/              # Database migrations
│   │   ├── env.py
│   │   ├── script.py.mako
│   │   └── versions/         # Migration files
│   │       ├── 001_initial_migration.py
│   │       └── 002_restructure_and_password_hashing.py
│   ├── favorites/            # Favorites (bookmarks) module
│   │   ├── __init__.py
│   │   ├── dao.py
│   │   ├── models.py         # Favorite model
│   │   ├── router.py
│   │   └── schemas.py
│   ├── movies/               # Movies module
│   │   ├── __init__.py
│   │   ├── dao.py
│   │   ├── models.py
│   │   ├── router.py
│   │   └── schemas.py
│   ├── reviews/              # Reviews module
│   │   ├── __init__.py
│   │   ├── dao.py
│   │   ├── models.py         # Review model
│   │   ├── router.py
│   │   └── schemas.py
│   ├── users/                # Users module
│   │   ├── __init__.py
│   │   ├── dao.py
│   │   ├── models.py
│   │   ├── router.py
│   │   └── schemas.py
│   ├── static/               # Frontend files
│   ├── config.py
│   ├── database.py           # Database configuration
│   ├── db.py                 # Database helper functions
│   └── main.py               # FastAPI app initialization
├── init_db.py                # Database initialization
├── seed_db.py                # Database seed data
├── run.py                    # Server entry point
├── requirements.txt          # Python dependencies
└── kinovzor.db               # SQLite database
```

## Database Layer (app/db.py)

The `db.py` file contains all database operations. It's designed to be modular and easy to extend.

### Password Hashing Functions

```python
from app.db import hash_password, verify_password

# Hash a password
hashed = hash_password("mypassword")

# Verify a password
if verify_password("mypassword", hashed):
    print("Password is correct")
```

### Users Database Functions

```python
from app.db import create_user, get_user_by_id, update_user, delete_user

# Create user (password auto-hashed)
user = create_user(
    email="user@example.com",
    password="securepass123",  # Auto-hashed
    username="johndoe"
)

# Get user by ID
user = get_user_by_id(1)

# Update user
user = update_user(
    user_id=1,
    email="newemail@example.com",
    username="newusername",
    password="newpass123"  # Auto-hashed
)

# Delete user (cascades delete reviews and favorites)
delete_user(1)
```

### Movies Database Functions

```python
from app.db import create_movie, get_movie_by_id, update_movie, delete_movie

# Create movie
movie = create_movie(
    title="Inception",
    description="A sci-fi thriller",
    genre="Sci-Fi",
    year=2010
)

# Get movie
movie = get_movie_by_id(1)

# Update movie
movie = update_movie(
    movie_id=1,
    title="Inception (Updated)",
    year=2011
)

# Delete movie (cascades delete reviews and favorites)
delete_movie(1)
```

### Reviews Database Functions

```python
from app.db import create_review, get_review_by_id, update_review, delete_review

# Create review
review = create_review(
    movie_id=1,
    user_id=1,
    text="Great movie!",
    rating=5
)

# Get review
review = get_review_by_id(1)

# Update review
review = update_review(
    review_id=1,
    text="Updated review text",
    rating=4
)

# Delete review
delete_review(1)
```

### Favorites Database Functions

```python
from app.db import add_favorite, remove_favorite, get_user_favorites, is_favorite

# Add to favorites
add_favorite(movie_id=1, user_id=1)

# Check if favorite
if is_favorite(movie_id=1, user_id=1):
    print("This is a favorite")

# Get user favorites
favorites = get_user_favorites(user_id=1)

# Remove favorite
remove_favorite(movie_id=1, user_id=1)
```

## API Testing

### Using cURL

**Register User:**
```bash
curl -X POST http://localhost:8000/api/users/register \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@example.com",
    "username": "testuser",
    "password": "testpass123"
  }'
```

**Update User:**
```bash
curl -X PUT http://localhost:8000/api/users/1 \
  -H "Content-Type: application/json" \
  -d '{
    "username": "newusername",
    "password": "newpass123"
  }'
```

**Delete User:**
```bash
curl -X DELETE http://localhost:8000/api/users/1
```

**Create Review:**
```bash
curl -X POST http://localhost:8000/api/reviews \
  -H "Content-Type: application/json" \
  -d '{
    "movie_id": 1,
    "user_id": 1,
    "text": "Great movie!",
    "rating": 5
  }'
```

**Update Review:**
```bash
curl -X PUT http://localhost:8000/api/reviews/1 \
  -H "Content-Type: application/json" \
  -d '{
    "text": "Updated review",
    "rating": 4
  }'
```

**Delete Movie:**
```bash
curl -X DELETE http://localhost:8000/api/movies/1
```

### Using Python Requests

```python
import requests

BASE_URL = "http://localhost:8000/api"

# Register
response = requests.post(f"{BASE_URL}/users/register", json={
    "email": "test@example.com",
    "username": "testuser",
    "password": "testpass123"
})
print(response.json())

# Update user
response = requests.put(f"{BASE_URL}/users/1", json={
    "username": "newusername"
})
print(response.json())

# Delete user
response = requests.delete(f"{BASE_URL}/users/1")
print(response.json())
```

## Database Migrations

### Create New Migration

```bash
cd app
alembic revision --autogenerate -m "description of changes"
```

This creates a new file in `app/alembic/versions/`

### Apply Migrations

```bash
cd app
alembic upgrade head      # Apply all pending migrations
alembic upgrade +1        # Apply next migration
alembic downgrade -1      # Rollback one migration
```

### View Migration History

```bash
cd app
alembic current            # Show current version
alembic history           # Show all versions
```

## Adding New Features

### Example: Add a new field to Movie

1. **Update model** (`app/movies/models.py`):
```python
from sqlalchemy import String

class Movie(Base):
    # ... existing fields ...
    director: Mapped[str] = mapped_column(String(255), nullable=True)
```

2. **Create migration**:
```bash
cd app
alembic revision --autogenerate -m "add director field to movies"
```

3. **Review and update generated migration** (if needed)

4. **Apply migration**:
```bash
alembic upgrade head
```

5. **Update database functions** (`app/db.py`):
```python
def update_movie(movie_id: int, ..., director: str = None) -> Dict:
    # Add director to update logic
    if director is not None:
        updates.append("director = ?")
        params.append(director)
```

6. **Update router** (`app/movies/router.py`):
```python
class MovieUpdate(BaseModel):
    # ... existing fields ...
    director: Optional[str] = None
```

## Testing Best Practices

### Test CRUD Operations

1. **Create** - Verify object is created with correct data
2. **Read** - Verify object can be retrieved
3. **Update** - Verify object fields are updated
4. **Delete** - Verify object is deleted and cascades work

### Test Password Hashing

```python
from app.db import hash_password, verify_password, create_user

# Test 1: Passwords are hashed
user = create_user(
    email="test@example.com",
    password="testpass123",
    username="testuser"
)
assert user['password'] != "testpass123"  # Should be hashed
assert len(user['password']) > 30  # Bcrypt produces ~60 char hash

# Test 2: Correct password verifies
password_correct = verify_password("testpass123", user['password'])
assert password_correct is True

# Test 3: Wrong password doesn't verify
password_wrong = verify_password("wrongpassword", user['password'])
assert password_wrong is False
```

### Test Cascade Delete

```python
from app.db import (
    create_movie, create_user, create_review,
    add_favorite, delete_movie, delete_user
)

# Create test data
movie = create_movie("Test", "Test movie", "Drama", 2025)
user = create_user("user@test.com", "pass123", "testuser")
review = create_review(movie['id'], user['id'], "Great!", 5)
add_favorite(movie['id'], user['id'])

# Delete movie should cascade
delete_movie(movie['id'])

# Verify review and favorite are deleted
assert get_review_by_id(review['id']) is None
assert is_favorite(movie['id'], user['id']) is False
```

## Code Style

### Python Style

- Use PEP 8 conventions
- Type hints for function parameters and returns
- Descriptive variable names
- Comments for complex logic

### Example:

```python
from typing import Optional, Dict, List

def update_user(user_id: int, email: str = None, username: str = None) -> Optional[Dict]:
    """Update user profile with optional fields.
    
    Args:
        user_id: ID of user to update
        email: New email (optional)
        username: New username (optional)
    
    Returns:
        Updated user dict or None if user not found
    """
    user = get_user_by_id(user_id)
    if not user:
        return None
    
    # Update logic here
    return user
```

## Troubleshooting

### Password Not Hashing

- Verify `create_user()` and `update_user()` are being used
- Check that passlib and bcrypt are installed: `pip list | grep passlib`

### Migration Conflicts

- Check current Alembic version: `alembic current`
- If stuck, reset migrations (backup first!): `alembic stamp head`

### Database Lock

- Close all connections to database
- Delete any `kinovzor.db-journal` files
- Restart server

### Cascade Delete Not Working

- Verify foreign key constraints are in place
- Check that cascade="all, delete-orphan" is set in relationship definitions

## Performance Tips

1. **Cache frequently accessed data**
   - Movie ratings are recalculated each time
   - Consider caching rating stats

2. **Batch operations**
   - Update multiple items in one transaction
   - Reduces database I/O

3. **Index frequently queried fields**
   - Email and username in users table
   - Movie ID and user ID in reviews

4. **Use pagination for large lists**
   - Limit results per request
   - Implement offset/limit parameters

## Contributing

When contributing:

1. Create feature branch: `git checkout -b feature/your-feature`
2. Make changes and test locally
3. Commit with descriptive messages: `git commit -m "feat: add new feature"`
4. Push to branch: `git push origin feature/your-feature`
5. Create Pull Request to `refactor/crud-operations`

## Resources

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [SQLAlchemy Documentation](https://docs.sqlalchemy.org/)
- [Alembic Documentation](https://alembic.sqlalchemy.org/)
- [Passlib Documentation](https://passlib.readthedocs.io/)
- [Bcrypt](https://github.com/pyca/bcrypt)

## Getting Help

- Check existing issues on GitHub
- Review MIGRATION_NOTES.md and API_CHANGES_V2.md
- See CHANGELOG.md for version history
- Check README.md for general information
