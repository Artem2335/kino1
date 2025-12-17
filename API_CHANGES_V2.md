# API Changes in v2.0.0

## New Endpoints

This document lists all NEW endpoints added in v2.0.0. For complete API documentation, see README.md.

### Users API

#### Update User Profile
```http
PUT /api/users/{user_id}
Content-Type: application/json

{
  "email": "newemail@example.com",
  "username": "newusername",
  "password": "newpassword123"
}

Response: 200
{
  "id": 1,
  "email": "newemail@example.com",
  "username": "newusername",
  "is_moderator": false,
  "is_admin": false,
  "created_at": "2025-12-17T18:00:00",
  "updated_at": "2025-12-17T18:20:00"
}
```

**Notes:**
- All fields are optional
- Password will be automatically hashed
- Email and username must be unique
- User can only update their own profile (in production, verified by JWT token)

#### Delete User Account
```http
DELETE /api/users/{user_id}

Response: 200
{
  "status": "deleted"
}
```

**Cascade Delete:**
- All user's reviews will be deleted
- All user's favorites will be deleted
- User record will be deleted

#### Get User by ID
```http
GET /api/users/{user_id}

Response: 200
{
  "id": 1,
  "email": "user@example.com",
  "username": "johndoe",
  "is_moderator": false,
  "is_admin": false,
  "created_at": "2025-12-17T18:00:00",
  "updated_at": "2025-12-17T18:00:00"
}
```

### Movies API

#### Delete Movie
```http
DELETE /api/movies/{movie_id}

Response: 200
{
  "status": "deleted"
}
```

**Cascade Delete:**
- All reviews for this movie will be deleted
- All favorites (bookmarks) for this movie will be deleted
- Movie record will be deleted

### Reviews API

#### Update Review
```http
PUT /api/reviews/{review_id}
Content-Type: application/json

{
  "text": "Updated review text here",
  "rating": 4
}

Response: 200
{
  "id": 42,
  "movie_id": 5,
  "user_id": 1,
  "text": "Updated review text here",
  "rating": 4,
  "approved": false,
  "username": "johndoe",
  "created_at": "2025-12-17T17:00:00",
  "updated_at": "2025-12-17T18:20:00"
}
```

**Notes:**
- Both fields are optional
- Only review author can update their review
- Rating should be between 1-5
- Update doesn't affect approval status

## Updated Endpoints

### Users API

#### Register (Enhanced)
```http
POST /api/users/register
Content-Type: application/json

{
  "email": "user@example.com",
  "username": "johndoe",
  "password": "securepassword123"
}

Response: 200
{
  "id": 1,
  "email": "user@example.com",
  "username": "johndoe",
  "is_moderator": false,
  "is_admin": false
}
```

**Changes:**
- ✅ Password is now automatically hashed using bcrypt
- ✅ Enhanced validation for duplicate email/username

#### Login (Updated)
```http
POST /api/users/login
Content-Type: application/json

{
  "username": "johndoe",
  "password": "securepassword123"
}

Response: 200
{
  "id": 1,
  "email": "user@example.com",
  "username": "johndoe",
  "is_moderator": false,
  "is_admin": false
}
```

**Changes:**
- ✅ Now verifies password using bcrypt hash
- ✅ More secure password comparison

### Movies API

#### Update Movie (Enhanced)
```http
PUT /api/movies/{movie_id}
Content-Type: application/json

{
  "title": "Updated Title",
  "description": "Updated description",
  "genre": "Drama",
  "year": 2024,
  "poster_url": "https://example.com/poster.jpg"
}

Response: 200
{
  "id": 5,
  "title": "Updated Title",
  "description": "Updated description",
  "genre": "Drama",
  "year": 2024,
  "poster_url": "https://example.com/poster.jpg"
}
```

**Changes:**
- ✅ Now returns updated movie object
- ✅ Better error handling

## Removed Endpoints

❌ **Ratings API** - No longer available

Instead, use review ratings:
- Include `rating` field when creating/updating reviews
- Get rating statistics: `GET /api/movies/{movie_id}` and check review ratings
- Calculate average from reviews: Each review has optional rating (1-5)

## Error Responses

All endpoints follow consistent error format:

```json
{
  "detail": "Error description message"
}
```

### Common Error Codes

**400 Bad Request**
```json
{
  "detail": "Email already exists"
}
```

**401 Unauthorized**
```json
{
  "detail": "Invalid credentials"
}
```

**403 Forbidden**
```json
{
  "detail": "Not authorized to update this user"
}
```

**404 Not Found**
```json
{
  "detail": "User not found"
}
```

## Authentication

⚠️ **Current Status:** No authentication implemented yet

- `user_id` and `current_user_id` parameters are for future JWT implementation
- For now, these should be passed as query parameters or headers
- Implement JWT tokens in future version for production security

### Example with Future JWT:
```http
PUT /api/users/1
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
Content-Type: application/json

{
  "username": "newusername"
}
```

## Migration from v1

If upgrading from v1.0.0:

1. **Backup your database**
   ```bash
   cp kinovzor.db kinovzor.db.backup
   ```

2. **Run migration**
   ```bash
   cd app
   alembic upgrade head
   ```

3. **Test new endpoints**
   - Try updating a user profile
   - Try deleting a movie
   - Try updating a review

4. **Update client code**
   - Add calls to new UPDATE/DELETE endpoints
   - Update password handling (already hashed)
   - Remove any Ratings API calls

## Password Security

Starting in v2.0.0, all passwords are automatically hashed:

```python
from app.db import hash_password, verify_password

# When user registers or updates password:
hashed = hash_password(user_password)  # Automatic in create_user/update_user

# When user logs in:
if verify_password(login_password, stored_hash):
    # Password is correct
    pass
```

**Algorithm:** bcrypt with secure salt generation

**For Existing Passwords:**
- If passwords were stored in plaintext in v1.0.0
- Recommend users to:
  1. Use "Forgot Password" feature (future)
  2. Or manually reset password through update endpoint
  3. On update, password will be automatically hashed

## Code Examples

### Create User with Hashed Password
```python
from app.db import create_user

# Password is automatically hashed
user = create_user(
    email="user@example.com",
    password="mysecurepassword",  # This will be hashed internally
    username="johndoe"
)
```

### Update User Password
```python
from app.db import update_user

# New password is automatically hashed
updated_user = update_user(
    user_id=1,
    password="newpassword123"  # This will be hashed internally
)
```

### Verify Password During Login
```python
from app.db import get_user_by_username, verify_password

user = get_user_by_username("johndoe")
if user and verify_password(input_password, user['password']):
    # Login successful
    print(f"Welcome {user['username']}!")
else:
    # Login failed
    print("Invalid credentials")
```

## Testing with cURL

### Create User
```bash
curl -X POST http://localhost:8000/api/users/register \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@example.com",
    "username": "testuser",
    "password": "testpass123"
  }'
```

### Update User
```bash
curl -X PUT http://localhost:8000/api/users/1 \
  -H "Content-Type: application/json" \
  -d '{
    "username": "newusername",
    "password": "newpass123"
  }'
```

### Delete User
```bash
curl -X DELETE http://localhost:8000/api/users/1
```

### Update Review
```bash
curl -X PUT http://localhost:8000/api/reviews/42 \
  -H "Content-Type: application/json" \
  -d '{
    "text": "Great movie!",
    "rating": 5
  }'
```

### Delete Movie
```bash
curl -X DELETE http://localhost:8000/api/movies/5
```

## Support

For more information:
- See MIGRATION_NOTES.md for detailed migration guide
- See README.md for complete API documentation
- Check app/db.py for database function documentation
