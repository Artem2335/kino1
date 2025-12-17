import sys
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from fastapi import FastAPI, status
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware
from starlette.requests import Request
from app.users.router import router as router_users
from app.movies.router import router as router_movies
from app.reviews.router import router as router_reviews
from app.favorites.router import router as router_favorites
from app import db
import os

# Initialize database if not exists
if not Path(__file__).parent.parent.joinpath('kinovzor.db').exists():
    print("\n📁 Database not found. Creating...")
    from init_db import init_db
    init_db()
    print("\n🍋 Loading seed data...")
    from seed_db import seed_movies_and_reviews
    seed_movies_and_reviews()
    print("\n✅ All ready!\n")

app = FastAPI(
    title="KinoVzor API",
    description="Movie review and rating platform",
    version="2.0.0"
)

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers FIRST (before static files)
app.include_router(router_users)
app.include_router(router_movies)
app.include_router(router_reviews)
app.include_router(router_favorites)

# Get the correct paths
STATIC_DIR = Path(__file__).parent / "static"
TEMPLATES_DIR = Path(__file__).parent / "templates"

# Setup Jinja2 templates BEFORE mounting static
if TEMPLATES_DIR.exists():
    templates = Jinja2Templates(directory=str(TEMPLATES_DIR))
    print(f"✅ Templates directory found at {TEMPLATES_DIR}")
else:
    print(f"\n⚠️ Warning: Templates directory not found at {TEMPLATES_DIR}")
    templates = None

# Root route - serve index.html from templates
@app.get('/')
async def root(request: Request):
    if templates:
        return templates.TemplateResponse("index.html", {"request": request})
    else:
        # Fallback if templates directory doesn't exist
        return RedirectResponse(url="/static/index.html", status_code=status.HTTP_303_SEE_OTHER)

# Compatibility route for old /static/index.html requests
@app.get('/static/index.html')
async def static_index(request: Request):
    """Redirect /static/index.html to / for backwards compatibility"""
    if templates:
        return templates.TemplateResponse("index.html", {"request": request})
    else:
        return RedirectResponse(url="/", status_code=status.HTTP_303_SEE_OTHER)

# Mount static files AFTER routes
if STATIC_DIR.exists():
    app.mount('/static', StaticFiles(directory=str(STATIC_DIR)), 'static')
    print(f"✅ Static directory found at {STATIC_DIR}")
else:
    print(f"\n⚠️ Warning: Static directory not found at {STATIC_DIR}")

if __name__ == "__main__":
    import uvicorn
    
    print("\n" + "="*50)
    print("🌟 KinoVzor - Movie Review Platform")
    print("="*50)
    print("\n🚀 Starting server...\n")
    
    uvicorn.run(
        "app.main:app",
        host="127.0.0.1",
        port=8000,
        reload=True
    )
