from pydantic import BaseModel
from datetime import datetime


class FavoriteCreate(BaseModel):
    movie_id: int
    user_id: int


class FavoriteResponse(BaseModel):
    id: int
    movie_id: int
    user_id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
