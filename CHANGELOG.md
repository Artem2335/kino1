# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [2.0.0] - 2025-12-17

### Added

**CRUD Operations:**
- Users: `PUT /api/users/{user_id}` - Update user profile (email, username, password)
- Users: `DELETE /api/users/{user_id}` - Delete user account with cascade delete
- Users: `GET /api/users/{user_id}` - Get user by ID
- Movies: `DELETE /api/movies/{movie_id}` - Delete movie with cascade delete
- Reviews: `PUT /api/reviews/{review_id}` - Update review text and rating
- Database: `update_user()` function with password hashing
- Database: `delete_user()` function with cascade delete
- Database: `update_movie()` function with dynamic fields
- Database: `delete_movie()` function with cascade delete
- Database: `update_review()` function

**Password Security:**
- Automatic password hashing using bcrypt in `create_user()` and `update_user()`
- Password verification function: `verify_password()`
- Enhanced password hashing utilities in `db.py`

**Code Organization:**
- New `app/favorites/models.py` - Favorite model in separate package
- New `app/reviews/models.py` - Review model in separate package
- Cleaned up `app/movies/models.py` - Removed inline Favorite/Review definitions
- Cleaned up `app/users/models.py` - Removed inline Favorite/Review definitions

**Database:**
- Alembic migration: `002_restructure_and_password_hashing.py`
- Migration drops ratings table (functionality moved to review ratings)
- Rating statistics calculated from review ratings via `get_rating_stats()`

**Documentation:**
- `MIGRATION_NOTES.md` - Comprehensive migration guide for v2.0.0
- `API_CHANGES_V2.md` - Detailed API documentation for new endpoints
- `CHANGELOG.md` - This file

### Changed

**API:**
- `PUT /api/movies/{movie_id}` now returns updated movie object
- Enhanced error handling across all CRUD operations
- Better validation for duplicate email/username

**Database:**
- Password hashing moved to database layer (automatic on create/update)
- Rating statistics calculation moved from ratings table to review ratings
- Review model now has proper foreign key constraints
- Favorite model now has proper foreign key constraints

**Project Structure:**
- `app/main.py` now includes routers for reviews and favorites
- Better separation of concerns with models in respective packages
- Enhanced database layer with CRUD operations

### Removed

**Database:**
- Ratings table (replaced with review ratings)
- Functions: `create_or_update_rating()`, `get_rating_by_id()`, `get_movie_ratings()`
- Ratings API endpoints (no longer available)

**Code:**
- Inline Favorite and Review model definitions from movies and users packages

### Fixed

- Password comparison now uses secure bcrypt verification instead of plaintext
- Database cascade deletes now properly handled for movie and user deletions
- Review model has proper foreign key constraints
- Favorite model has proper foreign key constraints

### Security

- ✅ All passwords are now automatically hashed using bcrypt
- ✅ Secure password verification for login
- ✅ Proper cascade delete to prevent orphaned data
- ⚠️ JWT authentication still needed for production (future)

### Breaking Changes

⚠️ **⚠️ Important for existing installations:**

1. **Ratings table removed**
   - Existing ratings data will be deleted by migration
   - Use review ratings going forward
   - Consider backing up database before migration

2. **Password hashing**
   - New passwords are hashed automatically
   - Existing plaintext passwords should be migrated
   - Consider running password migration script for existing users

3. **API changes**
   - Ratings endpoints removed
   - No breaking changes to existing endpoints
   - New endpoints available for UPDATE/DELETE operations

### Migration Guide

See `MIGRATION_NOTES.md` for:
- Step-by-step migration instructions
- Database backup procedures
- Alembic migration commands
- Password hashing best practices
- Testing checklist

### Dependencies

No new dependencies added. Already included:
- passlib (for password hashing)
- bcrypt (for secure hashing algorithm)
- alembic (for database migrations)

## [1.0.0] - 2025-12-12

### Added

**Initial Release:**
- User registration and login system
- Movie listing and details
- Review creation and management
- Favorites/bookmarks functionality
- Ratings system
- Moderator approval system
- Database models and migrations
- RESTful API endpoints
- SQLAlchemy ORM integration
- SQLite database support

**Features:**
- User authentication (basic)
- Movie catalog with filtering and sorting
- Review writing and rating
- Movie ratings calculation
- Favorites management
- Admin panel support
- Moderator tools

**API Endpoints:**
- Users: Register, Login, Get Profile
- Movies: Create, Read, List, Update
- Reviews: Create, Read, List, Delete, Approve
- Ratings: Create, Read, List
- Favorites: Add, Remove, List

**Database:**
- Users table with roles (user, moderator, admin)
- Movies table with metadata
- Reviews table with ratings
- Ratings table for separate ratings
- Favorites table for bookmarks
- Alembic migration system

**Documentation:**
- README.md with project overview
- INSTALL_GUIDE.md with setup instructions
- QUICK_START.md with quick start guide

---

## How to Upgrade

### From v1.0.0 to v2.0.0

```bash
# 1. Backup your database
cp kinovzor.db kinovzor.db.backup

# 2. Pull latest code
git pull origin refactor/crud-operations

# 3. Install dependencies (if any updates)
pip install -r requirements.txt

# 4. Run database migration
cd app
alembic upgrade head
cd ..

# 5. Restart server
python run.py
```

### Important Notes

- Ratings table will be deleted during migration
- Existing review ratings are preserved
- Passwords should be hashed (done automatically on update)
- New endpoints available for testing

## Version Comparison

| Feature | v1.0.0 | v2.0.0 |
|---------|--------|--------|
| User CRUD | Create, Read | Create, Read, Update, Delete |
| Movie CRUD | Create, Read, Update | Create, Read, Update, Delete |
| Review CRUD | Create, Read, Delete | Create, Read, Update, Delete |
| Password Hashing | ❌ | ✅ |
| Ratings Table | ✅ Separate | ❌ Removed (in reviews) |
| Code Organization | Mixed | Separated |
| Cascade Delete | Partial | Full |
| Database Migration | Basic | Versioned (002) |
| API Documentation | README | README + API_CHANGES_V2 |

## Next Steps (Future Versions)

- [ ] v2.1.0 - JWT Authentication
- [ ] v2.2.0 - Email verification
- [ ] v2.3.0 - Pagination and advanced filtering
- [ ] v2.4.0 - Caching layer
- [ ] v2.5.0 - Search functionality
- [ ] v3.0.0 - GraphQL API

---

**Last Updated:** 2025-12-17
