from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class ReviewBase(BaseModel):
    text: str
    rating: Optional[int] = None


class ReviewCreate(ReviewBase):
    movie_id: int
    user_id: int


class ReviewUpdate(BaseModel):
    text: Optional[str] = None
    rating: Optional[int] = None


class ReviewResponse(ReviewBase):
    id: int
    movie_id: int
    user_id: int
    approved: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
