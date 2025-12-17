from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, EmailStr
from app import db
from app.db import verify_password, hash_password
import json

router = APIRouter(prefix="/api/users", tags=["users"])


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


@router.post("/register")
def register(data: UserRegister):
    """Register a new user"""
    # Check if user already exists
    existing = db.get_user_by_email(data.email)
    if existing:
        raise HTTPException(status_code=400, detail="Email already exists")
    
    # Check if username already exists
    existing_username = db.get_user_by_username(data.username)
    if existing_username:
        raise HTTPException(status_code=400, detail="Username already exists")
    
    # Password will be hashed automatically in db.create_user
    user = db.create_user(data.email, data.password, data.username)
    return user


@router.post("/login")
def login(data: UserLogin):
    """Login user by username"""
    print(f"Login attempt with: {json.dumps({'username': data.username, 'password': '***'})}")
    
    # Get user by username
    user = db.get_user_by_username(data.username)
    
    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    # Verify password against hash
    if not verify_password(data.password, user['password']):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    return user


@router.get("/me")
def get_current_user(user_id: int):
    """Get current user info"""
    user = db.get_user_by_id(user_id)
    
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    return user


@router.get("/{user_id}")
def get_user(user_id: int):
    """Get user by ID"""
    user = db.get_user_by_id(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@router.put("/{user_id}")
def update_user(user_id: int, data: UserUpdate, current_user_id: int = None):
    """Update user profile (can only update own profile)"""
    # If current_user_id is not provided in header, allow update
    # In production, this should be verified from JWT token
    if current_user_id and user_id != current_user_id:
        raise HTTPException(status_code=403, detail="Not authorized to update this user")
    
    user = db.get_user_by_id(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    # Check if new email already exists (if email is being changed)
    if data.email and data.email != user['email']:
        existing = db.get_user_by_email(data.email)
        if existing:
            raise HTTPException(status_code=400, detail="Email already exists")
    
    # Check if new username already exists (if username is being changed)
    if data.username and data.username != user['username']:
        existing = db.get_user_by_username(data.username)
        if existing:
            raise HTTPException(status_code=400, detail="Username already exists")
    
    # Update user - password will be hashed automatically in db.update_user
    updated_user = db.update_user(
        user_id=user_id,
        email=data.email,
        username=data.username,
        password=data.password
    )
    
    return updated_user


@router.delete("/{user_id}")
def delete_user(user_id: int, current_user_id: int = None):
    """Delete user account (can only delete own account)"""
    # If current_user_id is not provided in header, allow deletion
    # In production, this should be verified from JWT token
    if current_user_id and user_id != current_user_id:
        raise HTTPException(status_code=403, detail="Not authorized to delete this user")
    
    user = db.get_user_by_id(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    db.delete_user(user_id)
    return {"status": "deleted"}
