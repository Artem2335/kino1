# KinoVzor v2.0.0 Migration Notes

## Overview
This document describes the major refactoring and restructuring done in v2.0.0 of the KinoVzor project.

## Key Changes

### 1. CRUD Operations Implementation

#### Users Module (`app/users/`)
- **CREATE**: ✅ Already existed - `/api/users/register` (POST)
- **READ**: ✅ Already existed - `/api/users/me` (GET), new `/api/users/{user_id}` (GET)
- **UPDATE**: ✨ NEW - `PUT /api/users/{user_id}` - Update email, username, password
- **DELETE**: ✨ NEW - `DELETE /api/users/{user_id}` - Delete user and cascade delete related data

#### Movies Module (`app/movies/`)
- **CREATE**: ✅ Already existed - `POST /api/movies`
- **READ**: ✅ Already existed - `GET /api/movies`, `GET /api/movies/{movie_id}`
- **UPDATE**: ✅ Already existed - `PUT /api/movies/{movie_id}`
- **DELETE**: ✨ NEW - `DELETE /api/movies/{movie_id}` - Delete movie and cascade delete all reviews and favorites

#### Reviews Module (`app/reviews/`)
- **CREATE**: ✅ Already existed
- **READ**: ✅ Already existed
- **UPDATE**: ✨ NEW - Update review text and rating
- **DELETE**: ✅ Already existed

### 2. Password Hashing

**All passwords are now automatically hashed in the database using bcrypt.**

- Password hashing happens in: `app/db.py::create_user()` and `app/db.py::update_user()`
- Uses `passlib` with bcrypt scheme
- Password verification: `app/db.py::verify_password()`
- Existing passwords in database should be manually hashed or reset by users

**New utility functions in `app/db.py`:**
- `hash_password(password: str) -> str`
- `verify_password(plain_password: str, hashed_password: str) -> bool`

### 3. Ratings Removal

**The standalone Ratings table has been removed.**

- Ratings functionality is now integrated into the Reviews model
- Each review has an optional `rating` field (1-5 stars)
- Rating statistics are calculated from approved review ratings
- New function: `app/db.py::get_rating_stats(movie_id)` - calculates average rating from reviews

**Database changes:**
- Ratings table (removed)
- Reviews table (already had `rating` column)

### 4. Code Reorganization

**Favorites and Reviews now have their own separate packages with models:**

```
app/
├── favorites/
│   ├── __init__.py
│   ├── dao.py
│   ├── models.py          ← NEW: Favorite model
│   ├── router.py
│   └── schemas.py
├── reviews/
│   ├── __init__.py
│   ├── dao.py
│   ├── models.py          ← NEW: Review model
│   ├── router.py
│   └── schemas.py
├── movies/
│   ├── __init__.py
│   ├── dao.py
│   ├── models.py          ← CLEANED: Removed inline Review/Favorite definitions
│   ├── router.py
│   └── schemas.py
├── users/
│   ├── __init__.py
│   ├── dao.py
│   ├── models.py          ← CLEANED: Removed inline Review/Favorite definitions
│   ├── router.py
│   └── schemas.py
└── main.py                ← UPDATED: Includes all 4 routers
```

**Benefits:**
- Better separation of concerns
- Easier to maintain and test
- Each module has its own models and database operations
- Cleaner dependency management

### 5. Database Layer Updates

**New functions in `app/db.py`:**

#### Users
- `update_user(user_id, email=None, username=None, password=None)` - Update user details
- `delete_user(user_id)` - Delete user and cascade delete reviews/favorites
- `hash_password(password)` - Hash password using bcrypt
- `verify_password(plain_password, hashed_password)` - Verify password

#### Movies
- `update_movie(movie_id, title=None, description=None, ...)` - Enhanced with dynamic fields
- `delete_movie(movie_id)` - Delete movie and cascade delete reviews/favorites

#### Reviews
- `update_review(review_id, text=None, rating=None)` - Update review details

#### Ratings (Removed)
- `create_or_update_rating()` - REMOVED
- `get_rating_by_id()` - REMOVED
- `get_movie_ratings()` - REMOVED
- `get_rating_stats()` - REPLACED with calculation from reviews

### 6. API Router Updates

#### `app/main.py`
```python
# Now includes all 4 routers:
app.include_router(router_users)
app.include_router(router_movies)
app.include_router(router_reviews)      ← NEW
app.include_router(router_favorites)    ← NEW
```

#### `app/users/router.py`
- Added: `PUT /api/users/{user_id}` - Update user profile
- Added: `DELETE /api/users/{user_id}` - Delete user account
- Added: `GET /api/users/{user_id}` - Get user by ID
- Improved username validation

#### `app/movies/router.py`
- Added: `DELETE /api/movies/{movie_id}` - Delete movie
- Fixed: Update endpoint to return updated movie

### 7. Database Migration

**Alembic migration created:** `app/alembic/versions/002_restructure_and_password_hashing.py`

**Changes:**
- Drops the `ratings` table
- Documents the restructuring
- Includes downgrade path for rollback

**To apply migration:**
```bash
cd app
alembic upgrade head
```

## Breaking Changes

⚠️ **Important for existing installations:**

1. **Ratings Table Removed**
   - Data in ratings table will be deleted
   - Consider backing up before migration
   - Use review ratings instead going forward

2. **Password Hashing**
   - All new passwords will be hashed
   - Existing plaintext passwords will still work if not updated
   - When updating passwords, they will be hashed
   - Consider running a migration script to hash existing passwords

3. **API Changes**
   - New endpoints available (UPDATE/DELETE)
   - No removal of existing endpoints
   - Backward compatible with existing code

## Installation & Setup

### Fresh Installation
1. Clone the repository from `refactor/crud-operations` branch
2. Install dependencies: `pip install -r requirements.txt`
3. Database will be initialized automatically on first run
4. Run migration: `alembic upgrade head` (from app/ directory)

### Existing Installation (Migration)
1. Backup your database: `cp kinovzor.db kinovzor.db.backup`
2. Pull changes: `git checkout refactor/crud-operations`
3. Install any new dependencies: `pip install -r requirements.txt`
4. Run migration: `cd app && alembic upgrade head`
5. Optional: Hash existing passwords using migration script

## New Dependencies

No new dependencies - `passlib` and `bcrypt` were already in requirements.txt

## Testing

### CRUD Operations Testing

```bash
# Users CRUD
POST /api/users/register        # Create
GET  /api/users/{user_id}       # Read
PUT  /api/users/{user_id}       # Update
DELETE /api/users/{user_id}     # Delete

# Movies CRUD
POST /api/movies                # Create
GET  /api/movies/{movie_id}     # Read
PUT  /api/movies/{movie_id}     # Update
DELETE /api/movies/{movie_id}   # Delete

# Reviews CRUD
POST /api/reviews               # Create
GET  /api/reviews/movies/{movie_id}  # Read
PUT  /api/reviews/{review_id}   # Update
DELETE /api/reviews/{review_id} # Delete

# Favorites CRUD
POST /api/favorites             # Add
GET  /api/users/{user_id}/favorites  # Read
DELETE /api/favorites           # Remove
```

### Password Hashing Test
```python
from app.db import hash_password, verify_password

hashed = hash_password("mypassword123")
assert verify_password("mypassword123", hashed)  # True
assert not verify_password("wrongpassword", hashed)  # False
```

## File Changes Summary

### Modified Files
- ✏️ `app/db.py` - Added CRUD operations, password hashing, updated Reviews functions
- ✏️ `app/users/router.py` - Added UPDATE/DELETE endpoints
- ✏️ `app/users/models.py` - Cleaned up, removed inline Favorite/Review definitions
- ✏️ `app/movies/router.py` - Added DELETE endpoint
- ✏️ `app/movies/models.py` - Cleaned up, removed inline Favorite/Review definitions
- ✏️ `app/main.py` - Updated to include all 4 routers
- ✏️ `app/reviews/models.py` - Updated foreign key constraints

### New Files
- ✨ `app/favorites/models.py` - Favorite model definition
- ✨ `app/reviews/models.py` - Review model definition (moved)
- ✨ `app/alembic/versions/002_restructure_and_password_hashing.py` - Migration
- ✨ `MIGRATION_NOTES.md` - This file

## Future Improvements

- [ ] Add JWT authentication
- [ ] Add email verification for new users
- [ ] Add refresh token mechanism
- [ ] Add comprehensive logging
- [ ] Add request/response validation middleware
- [ ] Add caching layer for movie ratings
- [ ] Add pagination to list endpoints
- [ ] Add search/filter functionality

## Support

For questions or issues related to this migration, please check:
1. Ensure you're on `refactor/crud-operations` branch
2. Check that all dependencies are installed
3. Verify Alembic migration ran successfully
4. Review the API documentation in README.md
