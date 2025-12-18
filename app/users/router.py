from fastapi import APIRouter, HTTPException, Response
from fastapi.responses import JSONResponse
from pydantic import BaseModel, EmailStr
from app import db
from passlib.context import CryptContext
from datetime import datetime, timedelta
import jwt
import json

router = APIRouter(prefix="/api/users", tags=["users"])

# JWT Configuration
SECRET_KEY = "your-secret-key"  # TODO: Move to .env
ALGORITHM = "HS256"
TOKEN_EXPIRE_HOURS = 24

# Password hashing context with flexible schemes to support old passwords
pwd_context = CryptContext(
    schemes=["bcrypt", "plaintext"],
    deprecated="auto",
    bcrypt__rounds=12
)


class UserRegister(BaseModel):
    email: EmailStr
    password: str
    username: str


class UserLogin(BaseModel):
    username: str
    password: str


class UserUpdate(BaseModel):
    email: EmailStr = None
    username: str = None
    password: str = None


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a password against its hash"""
    try:
        # Try standard verification first
        return pwd_context.verify(plain_password, hashed_password)
    except Exception as e:
        # If verification fails, try plaintext comparison as fallback
        # (for users created without proper hashing)
        try:
            return plain_password == hashed_password
        except:
            return False


def hash_password(password: str) -> str:
    """Hash a password"""
    return pwd_context.hash(password)


def create_jwt_token(user_id: int) -> str:
    """Create a JWT token for a user"""
    payload = {
        "user_id": user_id,
        "exp": datetime.utcnow() + timedelta(hours=TOKEN_EXPIRE_HOURS),
        "iat": datetime.utcnow()
    }
    token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)
    return token


@router.post("/register")
def register(data: UserRegister, response: Response):
    """Register a new user"""
    # Check if user already exists
    existing = db.get_user_by_email(data.email)
    if existing:
        raise HTTPException(status_code=400, detail="Email already exists")
    
    # Hash password
    hashed_password = hash_password(data.password)
    
    user = db.create_user(data.email, hashed_password, data.username)
    
    # Generate JWT token
    token = create_jwt_token(user['id'])
    
    # Set token in cookie
    response.set_cookie(
        key="access_token",
        value=token,
        max_age=TOKEN_EXPIRE_HOURS * 3600,
        httponly=True,
        samesite="lax"
    )
    
    return user


@router.post("/login")
def login(data: UserLogin, response: Response):
    """Login user by username"""
    print(f"Login attempt with: {json.dumps({'username': data.username, 'password': '***'})}")
    
    # Get user by username
    user = db.get_user_by_username(data.username)
    
    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    # Verify password against hash
    if not verify_password(data.password, user['password']):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    # Generate JWT token
    token = create_jwt_token(user['id'])
    
    # Set token in cookie
    response.set_cookie(
        key="access_token",
        value=token,
        max_age=TOKEN_EXPIRE_HOURS * 3600,
        httponly=True,
        samesite="lax"
    )
    
    return user


@router.get("/me")
def get_current_user(user_id: int):
    """Get current user info"""
    user = db.get_user_by_id(user_id)
    
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    return user


@router.put("/{user_id}")
def update_user(user_id: int, data: UserUpdate, current_user_id: int):
    """Update user profile (can only update own profile)"""
    # Check if user can update this profile
    if user_id != current_user_id:
        raise HTTPException(status_code=403, detail="Not authorized to update this user")
    
    user = db.get_user_by_id(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    # Check if new email already exists (if email is being changed)
    if data.email and data.email != user['email']:
        existing = db.get_user_by_email(data.email)
        if existing:
            raise HTTPException(status_code=400, detail="Email already exists")
    
    # Hash new password if provided
    hashed_password = None
    if data.password:
        hashed_password = hash_password(data.password)
    
    db.update_user(
        user_id=user_id,
        email=data.email,
        username=data.username,
        password=hashed_password
    )
    
    return db.get_user_by_id(user_id)


@router.delete("/{user_id}")
def delete_user(user_id: int, current_user_id: int):
    """Delete user account (can only delete own account)"""
    # Check if user can delete this profile
    if user_id != current_user_id:
        raise HTTPException(status_code=403, detail="Not authorized to delete this user")
    
    user = db.get_user_by_id(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    db.delete_user(user_id)
    return {"status": "deleted"}
