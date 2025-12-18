"""SQLAdmin configuration for the KinoVzor application."""

from sqladmin import Admin, ModelView, expose
from sqladmin.authentication import AuthenticationBackend
from app.database import engine
from app.users.models import User
from app.movies.models import Movie, Review, Favorite
from fastapi import FastAPI
from starlette.requests import Request
from starlette.responses import RedirectResponse
import os
from dotenv import load_dotenv

load_dotenv()

ADMIN_PASSWORD = os.getenv('ADMIN_PASSWORD', 'admin123')


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
    
    # Column visibility
    column_list = [User.id, User.username, User.email, User.is_admin, User.is_moderator, User.is_user, User.created_at]
    column_details_list = [User.id, User.username, User.email, User.password, User.is_admin, User.is_moderator, User.is_user, User.created_at, User.updated_at]
    column_searchable_list = [User.username, User.email]
    column_sortable_list = [User.id, User.username, User.created_at]
    column_default_sort = [(User.created_at, True)]
    
    # Exclude password from list view for security
    column_exclude_list = [User.password]
    
    # Form customization
    form_excluded_columns = [User.created_at, User.updated_at, User.reviews, User.favorites]


class MovieAdmin(ModelView, model=Movie):
    """Admin view for Movie model."""
    
    name = 'Movie'
    name_plural = 'Movies'
    icon = 'fa-solid fa-film'
    
    # Column visibility
    column_list = [Movie.id, Movie.title, Movie.genre, Movie.year, Movie.created_at]
    column_details_list = [Movie.id, Movie.title, Movie.description, Movie.genre, Movie.year, Movie.poster_url, Movie.created_at, Movie.updated_at]
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
    
    # Column visibility
    column_list = [Review.id, Review.movie_id, Review.user_id, Review.rating, Review.is_approved, Review.created_at]
    column_details_list = [Review.id, Review.movie_id, Review.user_id, Review.rating, Review.text, Review.is_approved, Review.created_at, Review.updated_at]
    column_searchable_list = [Review.text]
    column_sortable_list = [Review.id, Review.rating, Review.created_at, Review.is_approved]
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
    
    # Column visibility
    column_list = [Favorite.id, Favorite.user_id, Favorite.movie_id, Favorite.created_at]
    column_details_list = [Favorite.id, Favorite.user_id, Favorite.movie_id, Favorite.created_at]
    column_sortable_list = [Favorite.id, Favorite.created_at]
    column_default_sort = [(Favorite.created_at, True)]
    
    # Form customization
    form_excluded_columns = [Favorite.created_at]


def setup_admin(app: FastAPI) -> None:
    """Setup SQLAdmin for the FastAPI application.
    
    Args:
        app: FastAPI application instance
    """
    
    # Setup authentication
    authentication_backend = AdminUser()
    
    # Create admin instance
    admin = Admin(
        app=app,
        engine=engine,
        authentication_backend=authentication_backend,
        title='KinoVzor Admin',
        logo_url='https://img.icons8.com/color/96/000000/film.png',
        base_url='/admin',
    )
    
    # Register model views
    admin.register_model(UserAdmin)
    admin.register_model(MovieAdmin)
    admin.register_model(ReviewAdmin)
    admin.register_model(FavoriteAdmin)
