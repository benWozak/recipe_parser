from .instagram_routes import router as instagram_routes
from .user_routes import router as user_routes
from .household_routes import router as household_routes

__all__ = ["instagram_routes", "user_routes", "household_routes"]