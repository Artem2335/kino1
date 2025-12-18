"""SQLAdmin configuration for the KinoVzor application."""

from sqladmin import Admin, ModelView
from sqladmin.authentication import AuthenticationBackend
from starlette.requests import Request
from app.database import engine
from app.users.models import User
from app.movies.models import Movie
from app.reviews.models import Review
from app.favorites.models import Favorite
from fastapi import FastAPI
import os
from dotenv import load_dotenv

load_dotenv()

ADMIN_PASSWORD = os.getenv('ADMIN_PASSWORD', 'admin123')
SECRET_KEY = os.getenv('SECRET_KEY', 'your-secret-key-change-in-production')


class AdminUser(AuthenticationBackend):
    """Simple authentication backend for admin panel."""
    
    async def login(self, request: Request) -> bool:
        """Authenticate admin user."""
        form = await request.form()
        username = form.get('username')
        password = form.get('password')
        
        # Simple admin authentication (username: admin, password: from .env)
        if username == 'admin' and password == ADMIN_PASSWORD:
            request.session.update({'admin_user': 'admin'})
            return True
        return False
    
    async def logout(self, request: Request) -> bool:
        """Logout admin user."""
        request.session.clear()
        return True
    
    async def authenticate(self, request: Request) -> bool:
        """Check if user is authenticated."""
        if 'admin_user' not in request.session:
            return False
        return True


class UserAdmin(ModelView, model=User):
    """Admin view for User model."""
    
    name = 'User'
    name_plural = 'Users'
    icon = 'fa-solid fa-user'
    
    # Column visibility in list view (exclude password and relationships)
    column_exclude_list = [User.password, User.reviews, User.favorites]
    
    # Columns to show in detail view
    column_details_exclude_list = [User.password, User.reviews, User.favorites]
    
    # Searchable columns
    column_searchable_list = [User.username, User.email]
    
    # Sortable columns
    column_sortable_list = [User.id, User.username, User.created_at]
    column_default_sort = [(User.created_at, True)]
    
    # Form customization
    form_excluded_columns = [User.created_at, User.updated_at, User.reviews, User.favorites]


class MovieAdmin(ModelView, model=Movie):
    """Admin view for Movie model."""
    
    name = 'Movie'
    name_plural = 'Movies'
    icon = 'fa-solid fa-film'
    
    # Exclude relationships from display
    column_exclude_list = [Movie.reviews, Movie.favorites]
    column_details_exclude_list = [Movie.reviews, Movie.favorites]
    
    # Searchable and sortable columns
    column_searchable_list = [Movie.title, Movie.genre]
    column_sortable_list = [Movie.id, Movie.title, Movie.year, Movie.created_at]
    column_default_sort = [(Movie.created_at, True)]
    
    # Form customization
    form_excluded_columns = [Movie.created_at, Movie.updated_at, Movie.reviews, Movie.favorites]
    
    # Make description a larger text field
    form_overrides = {
        'description': 'TextAreaField',
    }


class ReviewAdmin(ModelView, model=Review):
    """Admin view for Review model."""
    
    name = 'Review'
    name_plural = 'Reviews'
    icon = 'fa-solid fa-star'
    
    # Exclude relationships
    column_exclude_list = []
    column_details_exclude_list = []
    
    # Searchable and sortable columns
    column_searchable_list = [Review.text]
    column_sortable_list = [Review.id, Review.rating, Review.created_at, Review.approved]
    column_default_sort = [(Review.created_at, True)]
    
    # Form customization
    form_excluded_columns = [Review.created_at, Review.updated_at]
    
    # Make text a larger text field
    form_overrides = {
        'text': 'TextAreaField',
    }


class FavoriteAdmin(ModelView, model=Favorite):
    """Admin view for Favorite model."""
    
    name = 'Favorite'
    name_plural = 'Favorites'
    icon = 'fa-solid fa-heart'
    
    # Exclude relationships
    column_exclude_list = []
    column_details_exclude_list = []
    
    # Sortable columns
    column_sortable_list = [Favorite.id, Favorite.created_at]
    column_default_sort = [(Favorite.created_at, True)]
    
    # Form customization
    form_excluded_columns = [Favorite.created_at]


def setup_admin(app: FastAPI) -> None:
    """Setup SQLAdmin for the FastAPI application.
    
    Args:
        app: FastAPI application instance
    """
    
    # Setup authentication with secret_key
    authentication_backend = AdminUser(secret_key=SECRET_KEY)
    
    # Create admin instance - models are registered via class inheritance
    admin = Admin(
        app=app,
        engine=engine,
        authentication_backend=authentication_backend,
        title='KinoVzor Admin',
        logo_url='https://img.icons8.com/color/96/000000/film.png',
        base_url='/admin',
    )
    
    # Add model views to admin
    admin.add_view(UserAdmin)
    admin.add_view(MovieAdmin)
    admin.add_view(ReviewAdmin)
    admin.add_view(FavoriteAdmin)
